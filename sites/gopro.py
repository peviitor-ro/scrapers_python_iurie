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
import re
import json


def scraper():
    """
    ... scrape data from Gopro scraper.
        https://jobs.gopro.com/en/pl
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }
    )

    url = "https://job-boards.greenhouse.io/embed/job_board?for=goprocareers&b=https%3A%2F%2Fjobs.gopro.com%2Fen%2Fpl"
    response = session.get(url, timeout=30)
    match = re.search(r'window\.__remixContext\s*=\s*({.*?});', response.text, re.DOTALL)
    if not match:
        return []

    data = json.loads(match.group(1))
    job_posts = data.get("state", {}).get("loaderData", {}).get("routes/embed.job_board", {}).get("jobPosts", {}).get("data", [])

    job_list = []

    for job in job_posts:
        location = job.get("location", "")
        title = job.get("title", "")
        absolute_url = job.get("absolute_url", "")
        department = job.get("department", {})
        department_name = department.get("name", "") if department else ""

        location_lower = location.lower()

        if "romania" in location_lower or "bucharest" in location_lower or "bucuresti" in location_lower:
            city = "Bucuresti" if any(x in location_lower for x in ("bucharest", "bucuresti")) else location
            job_list.append(
                Item(
                    job_title=title,
                    job_link=absolute_url,
                    company="Gopro",
                    country="România",
                    county=get_county_json(city),
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

    company_name = "Gopro"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/c/c3/GoPro_logo.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
