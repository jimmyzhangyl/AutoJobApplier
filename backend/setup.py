from setuptools import setup, find_packages

setup(
    name="auto_job_applier",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Essential for Flask Application
        "Flask==3.0.3",  # Core framework
        "Flask-Cors==4.0.1",  # Handling CORS (Cross-Origin Resource Sharing)
        "Flask-SocketIO==5.3.6",  # For WebSocket communication
        "Flask-Testing==0.8.1",  # For testing Flask applications
        "python-dotenv==1.0.1",  # For managing environment variables
        # Testing
        "pytest==8.2.2",  # Testing framework
        "pytest-mock==3.14.0",  # Plugin for using mocks in tests
        # Web Scraping
        "beautifulsoup4==4.12.3",  # Parsing HTML and XML documents
        "requests==2.31.0",  # Making HTTP requests
        "selenium==4.21.0",  # Web browser automation
        # SocketIO dependencies
        "python-socketio==5.11.2",  # Socket.IO for Python
        # Development Tools
        "pip-tools==7.4.1",  # For managing dependencies
    ],
)
