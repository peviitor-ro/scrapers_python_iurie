"""

Config for Dynamic Post Method -> For Json format!

Company ---> Gopro
Link ------> https://jobs.gopro.com/api/v1/jobs/external

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

"""

from __utils import (
    get_county_json,
    Item,
    UpdateAPI,
)
import requests
from urllib.parse import unquote


def scraper():
    """
    ... scrape data from Gopro scraper.
        https://jobs.gopro.com/en/pl
    """
    url = "https://jobs.gopro.com/api/appSearch"
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }
    )
    session.get("https://jobs.gopro.com/sanctum/csrf-cookie", timeout=30)
    xsrf_token = unquote(session.cookies.get("XSRF-TOKEN", ""))

    payload = {
        "query": "",
        "search_fields": {
            "title": {},
            "location": {},
            "category": {},
            "city_filter": {},
            "country_filter": {},
        },
        "result_fields": {
            "title": {"raw": {}},
            "location": {"raw": {}},
            "job_type": {"raw": {}},
            "content": {"snippet": {"fallback": True}},
            "category": {"raw": {}},
            "country_filter": {"raw": {}},
            "city_filter": {"raw": {}},
            "url": {"raw": {}},
        },
        "precision": 2,
        "page": {"size": 100, "current": 1},
        "filters": {
            "all": [
                {"any": [{"location": "Bucharest"}]},
                {"any": [{"group_id": 2082}]},
                {"any": [{"live": 1}]},
            ]
        },
        "facets": {
            "category": {"type": "value", "size": 30},
            "location": {"type": "value", "size": 30},
            "job_type": {"type": "value", "size": 30},
        },
    }
    response = session.post(
        url,
        headers={
            "Content-Type": "application/json",
            "X-XSRF-TOKEN": xsrf_token,
            "Origin": "https://jobs.gopro.com",
            "Referer": "https://jobs.gopro.com/en/pl",
        },
        json=payload,
        timeout=30,
    )
    post_data = response.json()

    job_list = []

    for job in post_data["results"]:
        city = (
            "Bucuresti"
            if "bucharest" in job["city_filter"]["raw"]
            else job["city_filter"]["raw"]
        )
        job_type = job["job_type"]["raw"].lower()

        # get jobs items from response
        job_list.append(
            Item(
                job_title=job["title"]["raw"],
                job_link="https://jobs.gopro.com/en/us/jobs/" + job["url"]["raw"],
                company="Gopro",
                country="România",
                county="all" if "remote" in job_type else get_county_json(city),
                city="all" if "remote" in job_type else city,
                remote=job_type,
            ).to_dict()
        )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Gopro"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/c/c3/GoPro_logo.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
