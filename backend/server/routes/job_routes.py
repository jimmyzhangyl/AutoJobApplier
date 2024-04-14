from flask import Blueprint, jsonify, request
from services.job_scraper_service import (
    scrape_seek_jobs,
    fetch_job_details,
    filter_jobs,
)

job_scraper_blueprint = Blueprint("job_scraper", __name__)


# TODO update this route method to POST later to accept search parameters
@job_scraper_blueprint.route("/scrap_jobs", methods=["GET"])
def scrap_jobs_route():
    search_params = {}  # define your search parameters
    filter_params = {"citizen", "clearance"}  # define your filter parameters
    search_source = "seek"  # define your search source
    job_ids = scrape_seek_jobs(search_params, filter_params, search_source)
    return {"job_ids": job_ids}


@job_scraper_blueprint.route("/job_details", methods=["GET"])
def test_details_route():
    filter_params = {"citizen", "clearance"}
    job_id = ["75008956"]  # NOTE: for test purposes only
    # job_details = fetch_job_details(job_id)  # call the fetch_job_details function
    filtered_result = filter_jobs(job_id, filter_params)
    return jsonify(filtered_result)
