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
    # Receiving data from the request
    data = request.json
    try:
        # Expecting passed in data aligned with data format of JobFilter
        search_filters = JobFilter(**data)
        logger.debug(f"Received search request with data: {search_filters}")
    except TypeError as e:
        logger.error(f"Error parsing search filters: {e}")
        return jsonify({"error": "Invalid search filters"}), 400

    # Passing the search filters to the job scraper service
    try:
        # FIXME: job source as a filter is not implemented yet
        result = search_seek_jobs_selenium(search_filters)
        logger.debug(f"Returning search results with {len(result)} jobs")
        return jsonify(result), 200
    # except JobScraperError as e:
    #     logger.error(f"Error during job search: {e}")
    #     return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500
