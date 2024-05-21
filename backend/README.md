# AutoJobApplier

Automate your next job application process

Backend framework: python/flask
Frontend framwork: Vue.js

## Prerequisites

- Python 3.8 or higher

## Installation Instructions - backend

1.Initiate virtual environment for python/flask:
run `python -m venv venv` under backend/

2.Activate the virtual environment.

- On Windows: `.\venv\Scripts\activate`
- On macOS/Linux:`source venv/bin/activate`

  3.Install the required dependencies.
  `pip install -r requirements.txt`

  4.Start the Flask application.
  `python server/app.py`

  0.Update requirement file
  -active the virtual environment
  -run `pip freeze > requirement.txt` in (venv) ..\AutoJobApplier\backend>

## DEBUG

in app.py, loading the corresponding .env.development for debug purpose, it will enable the logger.
API results will write to jobs.json and logger traces are located in app_debug.log

## Quick devolope TODO list
