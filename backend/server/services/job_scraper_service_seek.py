import requests
import json
import time
import logging
from bs4 import BeautifulSoup
from server.utils.socketio import socketio

SEEK_API_URL = "https://www.seek.com.au/api/chalice-search/v4/search"
logger = logging.getLogger(__name__)


def fetch_seek_jobs(location, keywords, page):
    params = {
        "where": location,
        "keywords": keywords,
        "page": page,
        "sortmode": "ListedDate",
    }
    try:
        logger.debug(f"Fetching jobs from Seek: {params}")
        response = requests.get(SEEK_API_URL, params=params)
        response.raise_for_status()
        logger.debug(f"Received response: {len(response.json().get('data', [])) > 0}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from Seek: {e}")
        return None


def apply_filters(job, filters):
    title_excludes = filters.get("titleExcludes", [])
    location_excludes = filters.get("locationExcludes", [])
    type_excludes = filters.get("typeExcludes", [])
    descrption_includes = filters.get("descriptionIncludes", [])
    descrption_exclude = filters.get("descriptionExcludes", [])

    if (
        title_excludes
        and title_excludes != [""]
        and any(
            exclude.lower() in job.get("title", "").lower()
            for exclude in title_excludes
        )
    ):
        logger.debug(f"Job {job['id']} excluded by title")
        return False
    if (
        location_excludes
        and location_excludes != [""]
        and any(
            exclude.lower() in job.get("location", "").lower()
            for exclude in location_excludes
        )
    ):
        logger.debug(f"Job {job['id']} excluded by location")
        return False
    if (
        type_excludes
        and type_excludes != [""]
        and any(
            exclude.lower() in job.get("workType", "").lower()
            for exclude in type_excludes
        )
    ):
        logger.debug(f"Job {job['id']} excluded by type")
        return False

    # Check if any of the exclusion criteria are met in the bullet points
    if descrption_exclude and descrption_exclude != [""]:
        # Iterate over each bullet point
        for point in job.get("bulletPoints", []):
            # Check each exclusion keyword against the current bullet point
            if any(exclude.lower() in point.lower() for exclude in descrption_exclude):
                logger.debug(
                    f"Job {job['id']} excluded by description exclude (bullet points)"
                )
                return False

    job_description = job.get("description", fetch_job_description(job["id"])).lower()

    if (
        descrption_exclude
        and descrption_exclude != [""]
        and any(exclude.lower() in job_description for exclude in descrption_exclude)
    ):
        logger.debug(f"Job {job['id']} excluded by description exclude")
        return False

    if (
        descrption_includes
        and descrption_includes != [""]
        and not any(
            include.lower() in job_description for include in descrption_includes
        )
    ):
        logger.debug(f"Job {job['id']} excluded by description include")
        return False
    logger.debug(f"Job {job['id']} passed all filters")
    return True


def fetch_job_description(job_id):
    job_detail_url = f"https://www.seek.com.au/job/{job_id}"
    try:
        logger.debug(f"Fetching job description for job ID: {job_id}")
        response = requests.get(job_detail_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        job_description = (
            soup.find("div", {"data-automation": "jobAdDetails"})
            .get_text(separator="\n")
            .strip()
        )
        logger.debug(f"Job description fetched: {len(job_description)>0}")
        return job_description
    except requests.RequestException as e:
        logger.error(f"Error fetching job description: {e}")
        return None
    except AttributeError as e:
        logger.error(f"Error parsing job description: {e}")
        return None


def support_quick_apply(job_id):
    job_detail_url = f"https://www.seek.com.au/job/{job_id}"
    try:
        logger.debug(f"checking support for quick apply: {job_id}")
        response = requests.get(job_detail_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        # Search for the text "Quick Apply" in the entire HTML document
        quick_apply_elements = soup.find_all(
            string=lambda text: "quick apply" in text.lower()
        )
        quick_apply_supported = len(quick_apply_elements) > 0

        logger.debug(f"Support for quick apply: {quick_apply_supported}")
        return quick_apply_supported
    except requests.RequestException as e:
        logger.error(f"Error fetching job apply: {e}")
        return None
    except AttributeError as e:
        logger.error(f"Error parsing job apply: {e}")
        return None


def save_job_data(jobs, filename="jobs.json"):
    with open(filename, "w") as file:
        json.dump(jobs, file)
    logger.debug(f"Saved job data to {filename}")


def search_jobs(data):
    location_includes = data.get("locationIncludes", [])
    title_includes = data.get("titleIncludes", "")
    filters = {
        "titleExcludes": (
            data.get("titleExcludes")
            if isinstance(data.get("titleExcludes"), list)
            else data.get("titleExcludes", "").split(",")
        ),
        "locationExcludes": (
            data.get("locationExcludes")
            if isinstance(data.get("locationExcludes"), list)
            else data.get("locationExcludes", "").split(",")
        ),
        "typeExcludes": (
            data.get("typeExcludes")
            if isinstance(data.get("typeExcludes"), list)
            else data.get("typeExcludes", "").split(",")
        ),
        "descriptionIncludes": (
            data.get("descriptionIncludes")
            if isinstance(data.get("descriptionIncludes"), list)
            else data.get("descriptionIncludes", "").split(",")
        ),
        "descriptionExcludes": (
            data.get("descriptionExcludes")
            if isinstance(data.get("descriptionExcludes"), list)
            else data.get("descriptionExcludes", "").split(",")
        ),
    }

    logger.debug(f"Starting job search with filters: {filters}")
    all_jobs = []
    page = 1
    max_retries = 3
    total_jobs = 0
    processed_jobs = 0

    while True:
        for attempt in range(max_retries):
            seek_response = fetch_seek_jobs(location_includes, title_includes, page)
            if seek_response:
                break
            logger.warning(f"Retry {attempt + 1} for fetching jobs")
            time.sleep(2)

        if not seek_response or not seek_response.get("data"):
            logger.debug("No more data from Seek or error in response")
            break

        jobs = seek_response.get("data", [])
        total_jobs = (
            min(seek_response.get("totalCount", 0), 20 * 27)
            if page == 1
            else total_jobs
        )
        if not jobs:
            logger.debug("No jobs found in response")
            break

        for job in jobs:
            processed_jobs += 1
            if apply_filters(job, filters):
                logger.debug(f"Job {job['id']} added to results")
                all_jobs.append(
                    {
                        "id": job.get("id", ""),
                        "title": job.get("title", ""),
                        "location": job.get("location", ""),
                        "listingDate": job.get("listingDate", ""),
                        "description": job.get(
                            "description", fetch_job_description(job["id"])
                        ),
                        "type": "auto" if support_quick_apply(job["id"]) else "manual",
                        "applyLink": f"https://www.seek.com.au/job/{job['id']}/apply",
                    }
                )

            # Send progress update
            remaining_jobs = total_jobs - processed_jobs
            estimated_time_left = remaining_jobs * 3
            progress_data = {
                "processed_jobs": processed_jobs,
                "total_jobs": total_jobs,
                "remaining_jobs": remaining_jobs,
                "estimated_time_left": estimated_time_left,
            }
            socketio.emit("job_progress", progress_data)

        page += 1

    save_job_data(all_jobs)
    logger.debug(f"Job search completed. Total jobs found: {len(all_jobs)}")
    return all_jobs
