import sys
import os
import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../server"))
)  # manual path insertion for the server package
from server.app import app as flask_app


@pytest.fixture
def client():
    return flask_app.test_client()
