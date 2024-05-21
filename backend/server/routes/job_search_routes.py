import logging
from flask import Blueprint, request, jsonify
from services.job_scraper_service_seek import search_jobs as search_seek_jobs

logger = logging.getLogger(__name__)

job_search_blueprint = Blueprint("job_search", __name__)

@job_search_blueprint.route("/", methods=["POST"])
def search_jobs_route():
    data = request.json
    logger.debug(f"Received search request with data: {data}")
    result = search_seek_jobs(data)
    logger.debug(f"Returning search results with {len(result)} jobs")
    return jsonify(result)
