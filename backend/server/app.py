from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.job_search_routes import job_search_blueprint
import os
import logging

# Load environment variables from .env file
load_dotenv(".env.development")

app = Flask(__name__)

# Enable CORS only in development environment
if os.getenv("FLASK_ENV") == "development":
    CORS(app)

# Set up logging
if os.getenv("FLASK_DEBUG") == "1":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app_debug.log",
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

logger = logging.getLogger(__name__)

app.register_blueprint(job_search_blueprint, url_prefix="/search")

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", port=os.getenv("FLASK_RUN_PORT"))
