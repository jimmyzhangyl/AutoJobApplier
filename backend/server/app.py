import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from models.extensions import socketio
from routes.job_search_routes import job_search_blueprint

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env.development"))

app = Flask(__name__)
CORS(app)

# Clear the console
os.system("cls" if os.name == "nt" else "clear")

# checking loaded environment variables
print(
    "\nLoaded environment variables: ",
    "Debug=",
    os.getenv("FLASK_DEBUG"),
    ",Port=",
    os.getenv("FLASK_RUN_PORT"),
)

# Set up logging
if os.getenv("FLASK_DEBUG") == "1":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app_debug.log",
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.debug("Logger initialized")
    print("Logger initialized: ", logger.name)

app.register_blueprint(job_search_blueprint, url_prefix="/search")

socketio.init_app(app)
print("Socketio initialized")

if __name__ == "__main__":
    socketio.run(
        app, debug=os.getenv("FLASK_DEBUG") == "1", port=os.getenv("FLASK_RUN_PORT")
    )
