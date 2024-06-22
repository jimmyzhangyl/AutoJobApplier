import logging
from flask import Blueprint, request, jsonify
from models.job_filter_model import JobFilter
from services.job_scraper_service_seek_selenium import (
    search_jobs as search_seek_jobs_selenium,
)

logger = logging.getLogger(__name__)

job_search_blueprint = Blueprint("job_search", __name__)


@job_search_blueprint.route("/", methods=["POST"])
def search_jobs_route():
    data = request.json
    try:
        search_filters = JobFilter(**data)
        logger.debug(f"Received search request with data: {search_filters}")
    except TypeError as e:
        logger.error(f"Error parsing search filters: {e}")
        return jsonify({"error": "Invalid search filters"}), 400
    # FIXME wrapped whole thing within try except block, so we can properly handle errors and status
    print(search_filters)
    result = search_seek_jobs_selenium(
        search_filters
    )  # FIXME returned value should be an array of Job objects
    logger.debug(f"Returning search results with {len(result)} jobs")
    return jsonify(result)  # FIXME give proper state of 200
