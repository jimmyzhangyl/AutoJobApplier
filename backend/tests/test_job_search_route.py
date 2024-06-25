import pytest
from flask import Flask
from flask.testing import FlaskClient
from server.routes.job_search_routes import job_search_blueprint
from server.models.job_filter_model import JobFilter
from tests.sample_data import valid_filter
from unittest.mock import patch


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(job_search_blueprint, url_prefix="/search")
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@patch("server.routes.job_search_routes.search_seek_jobs_selenium")
def test_search_jobs_route_valid(mock_search_jobs, client: FlaskClient, driver):
    mock_search_jobs.return_value = []

    response = client.post("/search/", json=valid_filter)

    assert response.status_code == 200
    assert response.json == []
    mock_search_jobs.assert_called_once()
    # Compare the attributes directly
    assert (
        mock_search_jobs.call_args[0][0].__dict__ == JobFilter(**valid_filter).__dict__
    )


@patch("server.routes.job_search_routes.search_seek_jobs_selenium")
def test_search_jobs_route_invalid(mock_search_jobs, client: FlaskClient, driver):
    invalid_data = {
        "titleIncludes": "Software",  # Invalid: should be a list
    }

    response = client.post("/search/", json=invalid_data)

    assert response.status_code == 400
    assert "Invalid search filters" in response.json["error"]


def test_search_jobs_route_internal_error(mocker, client: FlaskClient, driver):
    mock_search_jobs = mocker.patch(
        "server.routes.job_search_routes.search_seek_jobs_selenium"
    )
    mock_search_jobs.side_effect = Exception("Test error")

    response = client.post("/search/", json=valid_filter)

    assert response.status_code == 500
    assert "Internal server error" in response.json["error"]
    mock_search_jobs.assert_called_once()
    # Compare the attributes directly
    assert (
        mock_search_jobs.call_args[0][0].__dict__ == JobFilter(**valid_filter).__dict__
    )
