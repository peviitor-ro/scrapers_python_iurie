"""
Basic for scraping data from static pages.

Company ---> ENGIE
Link ------> https://jobs.engie.com/search/?q=&locationsearch=Romania
"""

import math

import requests

from __utils import Item, UpdateAPI, get_county_json


SEARCH_URL = "https://jobs.engie.com/services/recruiting/v1/jobs"
BASE_URL = "https://jobs.engie.com/job/"
PAGE_SIZE = 10


def _first_county(value):
    if isinstance(value, list):
        return value[0] if value else "all"
    return value or "all"


def _normalize_city(city):
    city = city.strip()
    replacements = {
        "Bucharest": "Bucuresti",
        "BUCURESTI": "Bucuresti",
        "Com Blejoi": "Blejoi",
        "Com. Blejoi": "Blejoi",
        "Ploiesti": "Ploiesti",
        "Turnu Magurele": "Turnu Magurele",
        "Targu Mures": "Targu Mures",
        "Ramnicu Valcea": "Ramnicu Valcea",
    }
    return replacements.get(city, city)


def _parse_locations(location_values):
    cities = []
    for value in location_values or []:
        parts = [part.strip() for part in value.split(",")]
        if len(parts) < 2 or parts[1].lower() != "romania":
            continue

        city = _normalize_city(parts[0])
        if city and city not in cities:
            cities.append(city)

    if len(cities) != 1:
        return "all", "all"

    city = cities[0]
    county = _first_county(get_county_json(city))
    return city, county


def _build_payload(page_number):
    return {
        "locale": "en_US",
        "pageNumber": page_number,
        "sortBy": "date",
        "keywords": "",
        "location": "Romania",
        "facetFilters": {},
        "brand": "",
        "skills": [],
        "categoryId": 0,
        "alertId": "",
        "rcmCandidateId": "",
    }


def scraper():
    """
    ... scrape data from ENGIE scraper.
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
            if not job_id or job_id in seen_ids:
                continue

            seen_ids.add(job_id)
            city, county = _parse_locations(data.get("jobLocationShort", []))

            job_list.append(
                Item(
                    job_title=data.get("unifiedStandardTitle"),
                    job_link=f"{BASE_URL}{data.get('urlTitle')}/{job_id}/",
                    company="ENGIE",
                    country="Romania",
                    county=county,
                    city=city,
                    remote="on-site",
                ).to_dict()
            )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "ENGIE"
    logo_link = "https://rmkcdn.successfactors.com/c4851ec3/1960b45a-f47f-41a6-b1c7-c.svg"

    jobs = scraper()
    print("Engie jobs", len(jobs))
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
