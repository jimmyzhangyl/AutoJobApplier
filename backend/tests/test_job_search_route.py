import pytest
from flask import Flask
from flask.testing import FlaskClient
from server.routes.job_search_routes import job_search_blueprint
from server.models.job_filter_model import JobFilter
from unittest.mock import patch, MagicMock


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(job_search_blueprint, url_prefix="/search")
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def test_search_jobs_route_valid(client: FlaskClient, mocker):
    mock_search_jobs = mocker.patch(
        "server.routes.job_search_routes.search_seek_jobs_selenium"
    )
    mock_search_jobs.return_value = []

    valid_data = {
        "titleIncludes": ["Software"],
        "titleExcludes": [],
        "locationIncludes": ["All Canberra ACT"],
        "locationExcludes": [],
        "typeExcludes": [],
        "descriptionIncludes": [],
        "descriptionExcludes": [],
        "jobSource": [],
        "daysListed": 1,
    }

    response = client.post("/search/", json=valid_data)

    assert response.status_code == 200
    assert response.json == []
    mock_search_jobs.assert_called_once()
    # Compare the attributes directly
    assert mock_search_jobs.call_args[0][0].__dict__ == JobFilter(**valid_data).__dict__


def test_search_jobs_route_invalid(client: FlaskClient):
    invalid_data = {
        "titleIncludes": "Software",  # Invalid: should be a list
    }

    response = client.post("/search/", json=invalid_data)

    assert response.status_code == 400
    assert "Invalid search filters" in response.json["error"]


def test_search_jobs_route_internal_error(client: FlaskClient, mocker):
    mock_search_jobs = mocker.patch(
        "server.routes.job_search_routes.search_seek_jobs_selenium"
    )
    mock_search_jobs.side_effect = Exception("Test error")

    valid_data = {
        "titleIncludes": ["Software"],
        "titleExcludes": [],
        "locationIncludes": ["All Canberra ACT"],
        "locationExcludes": [],
        "typeExcludes": [],
        "descriptionIncludes": [],
        "descriptionExcludes": [],
        "jobSource": [],
        "daysListed": 1,
    }

    response = client.post("/search/", json=valid_data)

    assert response.status_code == 500
    assert "Internal server error" in response.json["error"]
    mock_search_jobs.assert_called_once()
    # Compare the attributes directly
    assert mock_search_jobs.call_args[0][0].__dict__ == JobFilter(**valid_data).__dict__
