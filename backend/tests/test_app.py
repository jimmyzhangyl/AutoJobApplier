import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch
from server.app import create_app
from tests.sample_data import valid_filter


@pytest.fixture
def app() -> Flask:
    app = create_app(".env.development")
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@patch("server.app.load_environment")
@patch("server.app.setup_cors")
@patch("server.app.setup_logging")
@patch("server.app.setup_socketio")
@patch("server.app.start_server_with_socketio")
def test_app_initialization(
    mock_start_server,
    mock_setup_socketio,
    mock_setup_logging,
    mock_setup_cors,
    mock_load_environment,
):
    # Call the main function that initializes the app
    app = create_app(".env.development")

    # Ensure the functions were called with the correct arguments
    mock_load_environment.assert_called_once_with(".env.development")
    mock_setup_cors.assert_called_once_with(app)
    mock_setup_logging.assert_called_once()
    mock_setup_socketio.assert_called_once_with(app)
    mock_start_server.assert_not_called()  # Ensure the server start function is not called


# @patch("server.routes.job_search_routes.search_seek_jobs_selenium")
def test_app_blueprints(mocker, client: FlaskClient, driver):
    mock_search_jobs = mocker.patch(
        "server.routes.job_search_routes.search_seek_jobs_selenium"
    )
    mock_search_jobs.return_value = []
    response = client.post("/search/", json=valid_filter)

    assert response.status_code == 200
