import os
from flask_socketio import SocketIO


def get_cors_allowed_origins():
    if os.getenv("FLASK_DEBUG") == "1":
        return "*"
    else:
        # FIXME Set up CORS for production if needed
        return None


socketio = SocketIO(cors_allowed_origins=get_cors_allowed_origins())


def setup_socketio(app):
    socketio.init_app(app)
    print("Socketio initialized")


def start_server_with_socketio(app):
    socketio.run(
        app, debug=os.getenv("FLASK_DEBUG") == "1", port=os.getenv("FLASK_RUN_PORT")
    )
