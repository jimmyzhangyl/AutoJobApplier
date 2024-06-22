import os
import pytest
from flask import Flask
import logging
from server.app import app as flask_app
from flask_socketio import SocketIOTestClient, SocketIO


# Create a fixture for the Flask-SocketIO client
@pytest.fixture
def socketio_client():
    socketio = SocketIO(flask_app)
    return SocketIOTestClient(flask_app, socketio)


def test_home(client):
    response = client.get("/")
    assert response.status_code == 404
    # assert b"Hello, World!" in response.data


def test_logger_initialization():
    if os.getenv("FLASK_DEBUG") == "1":
        assert flask_app.logger.level == logging.DEBUG


def test_socketio_connection(socketio_client):
    socketio_client.connect()
    assert socketio_client.is_connected()
    socketio_client.disconnect()
    assert not socketio_client.is_connected()
