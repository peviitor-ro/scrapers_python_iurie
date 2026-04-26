"""
Company ---> wipro
Link ------> https://careers.wipro.com/search/?q=&locationsearch=Romania&searchResultView=LIST
"""

import math

import requests

from __utils import Item, UpdateAPI, get_county_json


SEARCH_URL = "https://careers.wipro.com/services/recruiting/v1/jobs"
BASE_URL = "https://careers.wipro.com/job/"
PAGE_SIZE = 10


def _first_county(value):
    if isinstance(value, list):
        return value[0] if value else "all"
    return value or "all"


def _normalize_city(raw_city):
    raw_city = raw_city.strip()
    if raw_city.startswith("Bucharest"):
        return "Bucuresti"
    if raw_city == "Timisoara":
        return "Timisoara"
    return raw_city or "all"


def _parse_locations(location_values):
    cities = []
    for value in location_values or []:
        city = _normalize_city(value.split(",", 1)[0])
        if city != "all" and city not in cities:
            cities.append(city)

    if len(cities) != 1:
        return "all", "all"

    city = cities[0]
    county = _first_county(get_county_json(city))
    return city, county


def _normalize_remote(job_title):
    lowered_title = job_title.lower()
    if "hybrid" in lowered_title:
        return "hybrid"
    if "remote" in lowered_title:
        return "remote"
    return "on-site"


def _build_payload(page_number):
    return {
        "keywords": "",
        "locale": "en_US",
        "location": "Romania",
        "pageNumber": page_number,
        "sortBy": "recent",
    }


def scraper():
    """
    ... scrape data from wipro scraper.
    https://careers.wipro.com/search/?q=&locationsearch=Romania&searchResultView=LIST
    """
    job_list = []
    seen_ids = set()

    first_page = requests.post(SEARCH_URL, json=_build_payload(0), timeout=30).json()
    total_jobs = first_page.get("totalJobs", 0)
    total_pages = math.ceil(total_jobs / PAGE_SIZE)

    for page_number in range(total_pages):
        response = first_page if page_number == 0 else requests.post(
            SEARCH_URL,
            json=_build_payload(page_number),
            timeout=30,
        ).json()

        for job in response.get("jobSearchResult", []):
            data = job.get("response", {})
            job_id = data.get("id")
            url_title = data.get("urlTitle") or data.get("unifiedUrlTitle")
            job_title = data.get("unifiedStandardTitle")
            if not job_id or not url_title or not job_title or job_id in seen_ids:
                continue

            seen_ids.add(job_id)
            city, county = _parse_locations(data.get("jobLocationShort", []))

            job_list.append(
                Item(
                    job_title=job_title,
                    job_link=f"{BASE_URL}{url_title}/{job_id}/",
                    company="wipro",
                    country="România",
                    county=county,
                    city=city,
                    remote=_normalize_remote(job_title),
                ).to_dict()
            )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "wipro"
    logo_link = "https://cms.jibecdn.com/prod/wipro/assets/HEADER-NAV_LOGO-en-us-1698423772812.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
