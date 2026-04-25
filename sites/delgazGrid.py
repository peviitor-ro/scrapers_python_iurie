"""
Basic for scraping data from static pages.

Company ---> Delgaz Grid
Link ------> https://careers.eon.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=RO&optionsFacetsDD_city=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield3=
"""

import re

import requests
from bs4 import BeautifulSoup

from __utils import Item, UpdateAPI, get_county_json


SEARCH_URL = "https://careers.eon.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=RO&optionsFacetsDD_city=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield3="
BASE_URL = "https://careers.eon.com"


def _first_county(value):
    if isinstance(value, list):
        return value[0] if value else "all"
    return value or "all"


def _normalize_location(city):
    city = (city or "").strip()

    if city in {"", "Romania"}:
        return "all", "all"
    if city == "Bucharest":
        city = "Bucuresti"
    if city in {"Telemuncă", "Telemunca"}:
        return "all", "all"

    county = _first_county(get_county_json(city))
    return city, county


def _normalize_remote(city, detail_text):
    city_value = (city or "").lower()
    if "telemunc" in city_value:
        return "remote"

    detail_lower = detail_text.lower()
    if "mod de lucru: remote" in detail_lower:
        return "remote"
    if "mod de lucru: hybrid" in detail_lower or "mod de lucru: hibrid" in detail_lower:
        return "hybrid"
    if "mod de lucru: birou/teren" in detail_lower:
        return "on-site"

    work_mode_match = re.search(r"Mod de lucru:\s*([^\n]+)", detail_text)
    if work_mode_match:
        work_mode = work_mode_match.group(1).strip().lower()
        if "remote" in work_mode:
            return "remote"
        if "hibrid" in work_mode or "hybrid" in work_mode:
            return "hybrid"
        if "birou/teren" in work_mode:
            return "on-site"

    return "on-site"


def scraper():
    """
    ... scrape data from Delgaz Grid scraper.
    """
    response = requests.get(SEARCH_URL, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    job_list = []
    for job in soup.find_all("div", class_="job"):
        link = job.find("a", class_="jobTitle-link", href=True)
        city_node = job.find("div", id=lambda value: isinstance(value, str) and value.endswith("-desktop-section-city-value"))
        if not link or not city_node:
            continue

        job_title = link.get_text(" ", strip=True)
        job_link = f"{BASE_URL}{link['href']}"
        city_value = city_node.get_text(" ", strip=True)

        detail_response = requests.get(job_link, timeout=30)
        detail_response.raise_for_status()
        detail_soup = BeautifulSoup(detail_response.text, "lxml")
        detail_text = detail_soup.get_text("\n", strip=True)

        if "Delgaz Grid" not in detail_text:
            continue

        city, county = _normalize_location(city_value)
        remote = _normalize_remote(city_value, detail_text)

        job_list.append(
            Item(
                job_title=job_title,
                job_link=job_link,
                company="Delgaz Grid",
                country="Romania",
                county=county,
                city=city,
                remote=remote,
            ).to_dict()
        )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Delgaz Grid"
    logo_link = "https://industrial-park.ro/wp-content/uploads/2019/05/delgaz-logo.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
