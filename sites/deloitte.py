"""
Basic for scraping data from static pages

Company ---> Deloitte
Link ------> https://apply.deloittece.com/en_US/careers/SearchJobs/?523=%5B5509%5D&523_format=1482&listFilterMode=1&jobRecordsPerPage=10&jobOffset=0

"""

import math
import re

import requests
import urllib3
from bs4 import BeautifulSoup

from __utils import Item, UpdateAPI, get_county_json, get_job_type


SEARCH_URL = "https://apply.deloittece.com/en_US/careers/SearchJobs/?523=%5B5509%5D&523_format=1482&listFilterMode=1&jobRecordsPerPage=10&jobOffset={offset}"
PAGE_SIZE = 10

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _get_soup(offset):
    response = requests.get(SEARCH_URL.format(offset=offset), verify=False, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def _extract_total_results(soup):
    legend = soup.find("div", class_="list-controls__text__legend")
    if not legend:
        return 0

    match = re.search(r"of\s+(\d+)\s+results", legend.get_text(" ", strip=True))
    return int(match.group(1)) if match else 0


def _normalize_location(location_text):
    location_text = location_text.replace(" - Romania", "").strip()
    cities = [city.strip() for city in location_text.split(",") if city.strip()]
    cities = ["Bucuresti" if city == "Bucharest" else city for city in cities]

    if len(cities) != 1:
        return "all", "all"

    city = cities[0]
    county = get_county_json(city)
    if isinstance(county, list):
        county = county[0] if county else "all"

    return city, county or "all"


def _normalize_remote(job_type_text):
    remote = get_job_type(job_type_text)
    if isinstance(remote, list):
        return remote[0] if remote else "on-site"
    return remote


def scraper():
    """
    ... scrape data from Deloitte scraper.
    https://apply.deloittece.com/en_US/careers/SearchJobs/?523=%5B5509%5D&523_format=1482&listFilterMode=1&jobRecordsPerPage=10&jobOffset=0
    """
    job_list = []
    first_page = _get_soup(0)
    total_results = _extract_total_results(first_page)
    pages = math.ceil(total_results / PAGE_SIZE)

    for page_index in range(pages):
        soup = first_page if page_index == 0 else _get_soup(page_index * PAGE_SIZE)

        for job in soup.find_all("div", class_="article__header__text"):
            anchor = job.find("a")
            span_elements = job.find_all("span")
            if not anchor or not span_elements:
                continue

            city, county = _normalize_location(span_elements[0].get_text(" ", strip=True))
            job_type_data = span_elements[-1].get_text(" ", strip=True)

            job_list.append(
                Item(
                    job_title=anchor.get_text(" ", strip=True),
                    job_link=anchor["href"],
                    company="Deloitte",
                    country="Romania",
                    county=county,
                    city=city,
                    remote=_normalize_remote(job_type_data),
                ).to_dict()
            )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Deloitte"
    logo_link = "https://logodownload.org/wp-content/uploads/2019/10/deloitte-logo.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
