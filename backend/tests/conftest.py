import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../server"))
)  # manual path insertion for the server package
from server.app import app as flask_app


@pytest.fixture
def client():
    return flask_app.test_client()


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
