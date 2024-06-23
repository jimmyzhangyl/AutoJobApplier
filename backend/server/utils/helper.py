import os
import logging
from dotenv import load_dotenv


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def check_loaded_environment_variables():
    print(
        "\nLoaded environment variables: ",
        "Debug=",
        os.getenv("FLASK_DEBUG"),
        ",Port=",
        os.getenv("FLASK_RUN_PORT"),
    )


def load_environment(env_file):
    # Path to the directory containing the .env files
    env_dir = os.path.join(os.path.dirname(__file__), "..")

    # Use the ".env.development" file for development or the ".env.production" file for production
    full_path = os.path.join(env_dir, env_file)
    load_dotenv(full_path)
    if env_file == ".env.development":
        clear_console()
        check_loaded_environment_variables()
        print("Environment variables loaded from ", env_file)


def setup_cors(app):
    from flask_cors import CORS

    if os.getenv("FLASK_DEBUG") == "1":
        CORS(app)
    else:
        # FIXME Set up CORS for production if needed
        print("CORS not enabled for production")
        pass


def setup_logging():
    if os.getenv("FLASK_DEBUG") == "1":
        logging.basicConfig(
            level=logging.DEBUG,
            filename="app_debug.log",
            filemode="w",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logger = logging.getLogger(
            __name__
        )  # __name__ is the name of the current module "utils.helper"
        logger.debug("Logger initialized")
        print("Logger initialized: ", logger.name)
    else:
        # FIXME Set up logging for production if needed
        print("Logging not enabled for production")
        pass
