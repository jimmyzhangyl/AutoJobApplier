# tests/conftest.py

import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../server"))
)

import pytest
from server.app import app as flask_app


@pytest.fixture
def client():
    return flask_app.test_client()
