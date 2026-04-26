"""
Company ---> Webasto
Link ------> https://jobs.webasto.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_location=&optionsFacetsDD_dept=&optionsFacetsDD_shifttype=&locationsearch=Romania&pageNumber=0&facetFilters=%7B%7D&sortBy=&markerViewed=&carouselIndex=
"""

from __utils import (
    get_county_json,
    Item,
    UpdateAPI,
)
import requests
import urllib3


SEARCH_URL = "https://jobs.webasto.com/services/recruiting/v1/jobs"
BASE_URL = "https://jobs.webasto.com/job/"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _first_county(value):
    if isinstance(value, list):
        return value[0] if value else "all"
    return value or "all"


def _parse_location(location_values):
    if not location_values:
        return "all", "all"

    parts = [part.strip() for part in location_values[0].split(",") if part.strip()]
    if len(parts) < 2:
        return "all", "all"

    city = parts[-3] if len(parts) >= 3 else parts[0]
    county = _first_county(get_county_json(city))
    return city, county


def scraper():
    """
    ... scrape data from Webasto scraper.
    """
    payload = {
        "keywords": "",
        "locale": "en_US",
        "location": "Romania",
        "pageNumber": 0,
        "sortBy": "recent",
    }
    response = requests.post(
        SEARCH_URL,
        headers={"Content-Type": "application/json"},
        json=payload,
        verify=False,
        timeout=30,
    )
    response.raise_for_status()
    response = response.json()

    job_list = []

    for job in response.get("jobSearchResult", []):
        data = job.get("response", {})
        job_id = data.get("id")
        url_title = data.get("urlTitle") or data.get("unifiedUrlTitle")
        if not job_id or not url_title:
            continue

        city, county = _parse_location(data.get("jobLocationShort", []))

        job_list.append(
            Item(
                job_title=data.get("unifiedStandardTitle"),
                job_link=f"{BASE_URL}{url_title}/{job_id}/",
                company="Webasto",
                country="România",
                county=county,
                city=city,
                remote="on-site",
            ).to_dict()
        )

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Webasto"
    logo_link = "https://logodix.com/logo/1699232.png"

    jobs = scraper()
    print("Jobs found", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
