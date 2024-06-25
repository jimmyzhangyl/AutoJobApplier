from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from models.job_filter_model import JobFilter

# example filters for reference
# filters = {
#     "titleIncludes": ["Software engineer","developer"]
#     "titleExcludes": ["lead", "senior"],
#     "locationIncludes": ["canberra-act"],
#     "locationExcludes": [""],
#     "typeExcludes": ["Part time", "Contract/Temp", "Casual/Vacation"],
#     "descriptionIncludes": [""],
#     "descriptionExcludes": ["nv1", "clearance", "citizenship"],
#     "jobSource": ["seek"],
#     "daysListed": "1",
# }


def get_selenium_driver():
    options = Options()
    # options.add_argument("--headless=new")
    # uncomment to choose which driver to use, usage: webdriver.Chrome(service=service, options=options)
    # driver_path = os.getenv("CHROMEDRIVER_PATH")
    # service = Service(driver_path)
    return webdriver.Chrome(options=options)


# Mapping user filters to Seek page urls
def get_search_page_urls(search_filters: JobFilter):
    # each locationIncludes needs an specifc url
    # each job titleIncludes needs a specific url
    # return combinations of both locations and job titles
    # dayslisted would be universal in seek, add to the end as daterange=daysListed
    urls = []
    for location in search_filters.locationIncludes:
        for title in search_filters.titleIncludes:
            url = f"https://www.seek.com.au/{title}-jobs/in-{location}?daterange={search_filters.daysListed}&sortmode=ListedDate"
            urls.append(url)
    return urls


def get_job_details(web_driver):
    job_details = {
        "title": "",
        "id": "",
        "location": "",
        "description": "",
    }


def search_jobs(search_filters: JobFilter):
    web_driver = get_selenium_driver()
    urls = get_search_page_urls(search_filters)
    try:
        for url in urls:
            web_driver.get(url)
            WebDriverWait(web_driver, 10)
            # scrape the page
            # input("Holding window open for debugging, Press Enter to continue...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        web_driver.quit()
    return "hit the search_jobs_selenium endpoint"
