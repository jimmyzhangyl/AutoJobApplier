import requests
import time
import random
import concurrent.futures
from bs4 import BeautifulSoup
import time

RETRY_LIMIT = 10


def scrape_seek_jobs(search_params, filter_params, search_source):
    start_time = time.time()

    seek_job_ids = get_job_ids()
    filtered_job_ids = filter_jobs(seek_job_ids, filter_params)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total extracted job ids: {len(seek_job_ids)}")
    print(f"Total filtered job ids: {len(filtered_job_ids)}")
    print(f"Total time spent: {total_time} seconds")

    return filtered_job_ids


def fetch_job_summary(page_number):
    # TODO because of the limitation of the Seek API, we can only fetch up to 27 pages of data, so we will search by two terms and combine the results(to limit the returned data within 27 pages)
    base_url = "https://www.seek.com.au/api/chalice-search/v4/search"
    params = {
        "siteKey": "AU-Main",
        "where": "All Canberra ACT",
        "page": page_number,
        "keywords": "software engineer",
        "locale": "en-AU",
    }
    headers = {
        "accept": "application/json, text/plain, */*",
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def extract_job_ids(data):
    ids = []
    for job in data:
        ids.append(job["id"])
    return ids


def get_job_ids():
    # TODO implement search for other sources
    # Seek API can only return up to 27 pages of data, on page number 28 it will return 404
    seek_job_ids = []

    # TODO swap the hardcoded range with a dynamic range based on the number of pages available, but up to 28 pages
    for page_number in range(1, 28):
        retry_count = 0
        while retry_count < RETRY_LIMIT:
            data = fetch_job_summary(page_number)
            job_ids = extract_job_ids(data)
            # Seek default pagination lists 20 jobs per page, unless it is the last page
            if len(data) >= 20 or len(data) > 0 and retry_count == (RETRY_LIMIT - 1):
                seek_job_ids.extend(job_ids)
                print(
                    f"Page {page_number} extracted successfully, fetched {len(job_ids)} job ids"
                )
                break
            else:
                retry_count += 1
                print(
                    f"No data found on page {page_number}, retrying ({retry_count}/{RETRY_LIMIT})"
                )
                time.sleep(random.uniform(0, 0.3))  # Add random delay between retries

        if retry_count == RETRY_LIMIT:
            print(f"No data found on page {page_number} after {RETRY_LIMIT} retries")

    # TODO store the job ids in a database
    return seek_job_ids


def fetch_job_details(job_id):
    url = f"https://www.seek.com.au/job/{job_id}"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

    for _ in range(RETRY_LIMIT):
        response = requests.get(url, headers=headers)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            # return response.json()
            soup = BeautifulSoup(response.text, "html.parser")
            # Find the div with the specific data-automation attribute
            job_details_div = soup.find(
                "div", attrs={"data-automation": "jobAdDetails"}
            )
            if job_details_div:
                # Extract and return the concatenated text of the div
                return job_details_div.get_text(separator=" ", strip=True)
            else:
                return "Job details not found."

        else:
            print(f"Failed to fetch job details for job ID {job_id}. Retrying...")
            time.sleep(random.uniform(0, 0.3))  # Add random delay between retries

    print(
        f"Failed to fetch job details for job ID {job_id} after {RETRY_LIMIT} retries"
    )
    return None


def filter_jobs(job_ids, filter_params):
    filtered_job_ids = []

    # Define a helper function to use with threading
    def process_job(job_id):
        job_details = fetch_job_details(job_id)
        if job_details and not any(
            param in job_details.lower() for param in filter_params
        ):
            return job_id, job_details[:20], True
        return job_id, None, False

    # Use ThreadPoolExecutor to handle multiple jobs in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the job_ids to the executor, processing them concurrently
        futures = {executor.submit(process_job, job_id): job_id for job_id in job_ids}
        total_jobs = len(job_ids)
        completed_jobs = 0

        for future in concurrent.futures.as_completed(futures):
            job_id = futures[future]
            try:
                result_job_id, job_preview, is_valid = future.result()
                if is_valid:
                    filtered_job_ids.append(result_job_id)
                    print(f"Valid job ID: {result_job_id}")
                    print(f"First 20 chars from job details: {job_preview}")
                else:
                    print(
                        f"Invalid job ID: {job_id}. Filter keyword(s) found: {', '.join(filter_params)}"
                    )
            except Exception as exc:
                print(f"Job ID {job_id} generated an exception: {exc}")
            completed_jobs += 1
            print(f"Progress: {completed_jobs}/{total_jobs}")

    # Calculate statistics
    valid_jobs = len(filtered_job_ids)
    invalid_jobs = total_jobs - valid_jobs
    valid_ratio = (valid_jobs / total_jobs) * 100
    invalid_ratio = (invalid_jobs / total_jobs) * 100
    print(f"Total valid jobs: {valid_jobs} ({valid_ratio:.2f}% of total)")
    print(f"Total invalid jobs: {invalid_jobs} ({invalid_ratio:.2f}% of total)")

    return filtered_job_ids
