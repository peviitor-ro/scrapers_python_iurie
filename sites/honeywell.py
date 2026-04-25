#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Honeywell
# Link ------> https://careers.honeywell.com/en/sites/Honeywell/jobs?location=Romania&locationId=300000000469737&locationLevel=country&mode=location
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from math import ceil
from __utils import (
    get_county_json,
    Item,
    UpdateAPI,
)
import requests


BASE_URL = "https://ibqbjb.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest"
LOCATION_ID = "300000000469737"
SITE_NUMBER = "CX_1"
PAGE_SIZE = 25


def get_city_and_county(primary_location: str):
    location = (primary_location or "").replace(", Romania", "").strip()
    parts = [part.strip() for part in location.split(",") if part.strip()]

    if not parts:
        return "all", "all"

    if len(parts) == 1 and parts[0] == "Romania":
        return "all", "all"

    city = "Bucuresti" if parts[0] == "Bucuresti" else parts[0]
    county = get_county_json(city)
    if isinstance(county, list):
        county = county[0] if county else None

    if county:
        return city, county

    return "all", "all"


def get_remote(workplace_type: str):
    mapping = {
        "Hybrid": "hybrid",
        "Remote": "remote",
        "On-site": "on-site",
    }
    return mapping.get(workplace_type, "on-site")


def fetch_jobs(offset: int):
    url = (
        f"{BASE_URL}/recruitingCEJobRequisitions"
        f"?onlyData=true"
        f"&expand=requisitionList.secondaryLocations"
        f"&finder=findReqs;siteNumber={SITE_NUMBER},limit={PAGE_SIZE},locationId={LOCATION_ID},offset={offset}"
    )
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Accept-Language": "en",
            "Ora-Irc-Language": "en",
        },
        timeout=30,
    )
    return response.json()["items"][0]


def scraper():
    '''
    ... scrape data from Honeywell scraper.
    '''
    first_page = fetch_jobs(0)
    total_jobs = first_page["TotalJobsCount"]
    pages = ceil(total_jobs / PAGE_SIZE)

    all_jobs = first_page.get("requisitionList", [])
    for page in range(1, pages):
        all_jobs.extend(fetch_jobs(page * PAGE_SIZE).get("requisitionList", []))

    job_list = []
    for job in all_jobs:
        primary_location = job.get("PrimaryLocation") or ""
        if "Romania" not in primary_location and job.get("PrimaryLocationCountry") != "RO":
            continue

        city, county = get_city_and_county(primary_location)

        job_list.append(
            Item(
                job_title=job["Title"],
                job_link="https://careers.honeywell.com/en/sites/Honeywell/job/" + job["Id"],
                company="Honeywell",
                country="România",
                county=county,
                city=city,
                remote=get_remote(job.get("WorkplaceType")),
            ).to_dict()
        )

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Honeywell"
    logo_link = "https://www.honeywell.com/content/dam/honeywellbt/en/images/logos/HON%20logo_200x37%202.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
