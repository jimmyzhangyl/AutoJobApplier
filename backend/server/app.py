from flask import Flask
from routes.job_search_routes import job_search_blueprint
from utils.helper import load_environment, setup_cors, setup_logging
from utils.socketio import setup_socketio, start_server_with_socketio


def create_app(env):
    app = Flask(__name__)

    # use the ".env.development" file for development or the ".env.production" file for production
    load_environment(env)

    setup_cors(app)
    setup_logging()
    setup_socketio(app)

    # Route binding
    app.register_blueprint(job_search_blueprint, url_prefix="/search")

    return app


app = create_app(".env.development")

if __name__ == "__main__":
    start_server_with_socketio(app)
