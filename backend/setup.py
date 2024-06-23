from setuptools import setup, find_packages

setup(
    name="auto_job_applier",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask==3.0.3",
        "Flask-Cors==4.0.1",
        "Flask-SocketIO==5.3.6",
        "python-dotenv==1.0.1",
        "selenium==4.21.0",
        "requests==2.31.0",
        "Werkzeug==3.0.2",
    ],
)
