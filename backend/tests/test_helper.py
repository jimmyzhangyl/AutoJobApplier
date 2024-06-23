import os
from unittest.mock import patch, MagicMock

# Import the helper functions
from server.utils.helper import (
    clear_console,
    check_loaded_environment_variables,
    load_environment,
    setup_cors,
    setup_logging,
)


@patch("server.utils.helper.os.system")
def test_clear_console(mock_system):
    clear_console()
    if os.name == "nt":
        mock_system.assert_called_once_with("cls")
    else:
        mock_system.assert_called_once_with("clear")


@patch("server.utils.helper.os.getenv")
def test_check_loaded_environment_variables(mock_getenv, capsys):
    mock_getenv.side_effect = lambda k: "1" if k == "FLASK_DEBUG" else "5000"
    check_loaded_environment_variables()
    captured = capsys.readouterr()
    assert "Loaded environment variables" in captured.out
    assert "Debug= 1" in captured.out
    assert "Port= 5000" in captured.out


@patch("server.utils.helper.load_dotenv")
@patch("server.utils.helper.clear_console")
@patch("server.utils.helper.check_loaded_environment_variables")
def test_load_environment(mock_check, mock_clear, mock_load):
    env_file = ".env.development"
    load_environment(env_file)

    mock_load.assert_called_once()
    mock_clear.assert_called_once()
    mock_check.assert_called_once()


@patch("flask_cors.CORS")
def test_setup_cors(mock_cors, monkeypatch):
    mock_app = MagicMock()
    monkeypatch.setenv("FLASK_DEBUG", "1")
    setup_cors(mock_app)
    mock_cors.assert_called_once_with(mock_app)

    monkeypatch.setenv("FLASK_DEBUG", "0")
    with patch("builtins.print") as mock_print:
        setup_cors(mock_app)
        mock_print.assert_called_once_with("CORS not enabled for production")


@patch("server.utils.helper.logging.basicConfig")
@patch("server.utils.helper.logging.getLogger")
def test_setup_logging(mock_get_logger, mock_basic_config, monkeypatch):
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger
    monkeypatch.setenv("FLASK_DEBUG", "1")
    with patch("builtins.print") as mock_print:
        setup_logging()
        mock_basic_config.assert_called_once()
        mock_get_logger.assert_called_once_with(
            "server.utils.helper"
        )  # Assuming logger is initialized in the helper module
        mock_logger.debug.assert_called_once_with("Logger initialized")
        mock_print.assert_called_once_with("Logger initialized: ", mock_logger.name)
    monkeypatch.setenv("FLASK_DEBUG", "0")
    with patch("builtins.print") as mock_print:
        setup_logging()
        mock_print.assert_called_once_with("Logging not enabled for production")
