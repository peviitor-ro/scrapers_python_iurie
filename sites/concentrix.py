"""
Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> Concentrix
Link ------> https://jobs.concentrix.com/job-search/?keyword=&country=Romania

"""

from __utils import (
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
import requests
from requests import HTTPError
from bs4 import BeautifulSoup


def scraper():
    """
    ... scrape data from Concentrix scraper.
    """
    url = "https://jobs.concentrix.com/wp-admin/admin-ajax.php"

    payload = "action=gd_jobs_query_pagination&country%5B%5D=Romania&keyword=&jobs_shown=0&jobs_per_page=50&wh=false"

    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Cookie": "__cf_bm=Eulwr4cnl4nSz42e4pW6pBBsuP0CpdA8Fgny9LoQyPk-1740473978-1.0.1.1-CRHhcFXSGDtPFw2PAzGTBIV4ZeJvCf9sZ2iodo2KLpp.zOrtHCRJgCz1ObRH34GxaWW2fNqJW.sX45yFkMkICw",
    }
    try:
        response = requests.post(url=url, data=payload, headers=headers)
        html = response.json().get("data").get("output")
        soup = BeautifulSoup(html, "lxml")

        job_list = []
        for job in soup.find_all("div", class_="job"):
            title = job.find("h3").text
            clean_title = title.split(" –")[0].split(" - ")[0]
            location = job.find("div", attrs="job-location").text.split(", R")[0]
            # change Bucharest to București
            if location == "Bucharest":
                location = "București"
            if location == "Targu":
                location = "Cluj"
            # get county for location
            county = get_county_json(location)
            # get jobs items from response
            job_list.append(
                Item(
                    job_title=clean_title,
                    job_link=job.find("a")["href"],
                    company="Concentrix",
                    country="România",
                    county=county,
                    city=location,
                    remote=get_job_type(title),
                ).to_dict()
            )
    except (HTTPError, ValueError) as e:
        print("Somethink went wrong", e)

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Concentrix"
    logo_link = "https://jobs.concentrix.com/wp-content/themes/jobswh/img/logo-concentrix-color.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
