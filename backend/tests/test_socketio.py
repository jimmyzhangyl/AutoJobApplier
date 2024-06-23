from unittest.mock import patch, MagicMock
from server.utils.socketio import (
    get_cors_allowed_origins,
    setup_socketio,
    start_server_with_socketio,
)


@patch("server.utils.socketio.os.getenv")
def test_get_cors_allowed_origins_debug(mock_getenv):
    mock_getenv.return_value = "1"
    assert get_cors_allowed_origins() == "*"


@patch("server.utils.socketio.os.getenv")
def test_get_cors_allowed_origins_production(mock_getenv):
    mock_getenv.return_value = "0"
    assert get_cors_allowed_origins() is None


@patch("server.utils.socketio.socketio.init_app")
def test_setup_socketio(mock_init_app):
    mock_app = MagicMock()
    with patch("builtins.print") as mock_print:
        setup_socketio(mock_app)
        mock_init_app.assert_called_once_with(mock_app)
        mock_print.assert_called_once_with("Socketio initialized")


@patch("server.utils.socketio.socketio.run")
@patch("server.utils.socketio.os.getenv")
def test_start_server_with_socketio(mock_getenv, mock_run):
    mock_getenv.side_effect = lambda key: "1" if key == "FLASK_DEBUG" else "5000"
    mock_app = MagicMock()
    start_server_with_socketio(mock_app)
    mock_run.assert_called_once_with(mock_app, debug=True, port="5000")
