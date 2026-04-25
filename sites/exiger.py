"""
Basic for scraping data from static pages.

Company ---> Exiger
Link ------> https://boards.greenhouse.io/embed/job_board?for=exiger&b=https%3A%2F%2Fwww.exiger.com%2Fcareers%2F
"""

import json
import re

import requests

from __utils import Item, UpdateAPI


BOARD_URL = "https://job-boards.greenhouse.io/embed/job_board?for=exiger&b=https%3A%2F%2Fwww.exiger.com%2Fcareers%2F"


def _load_jobs():
    response = requests.get(BOARD_URL, timeout=30)
    response.raise_for_status()

    match = re.search(r'window\.__remixContext\s*=\s*(\{.*?\});</script>', response.text, re.S)
    if not match:
        return []

    data = json.loads(match.group(1))
    return data["state"]["loaderData"]["routes/embed.job_board"]["jobPosts"]["data"]

def scraper():
    """
    ... scrape data from Exiger scraper.
    """
    jobs = _load_jobs()

    job_list = []
    for job in jobs:
        location = (job.get("location") or "").lower()
        if "romania" not in location and "bucharest" not in location and "bucure" not in location:
            continue

        job_list.append(
            Item(
                job_title=job.get("title", "").strip(),
                job_link=job.get("absolute_url"),
                company="Exiger",
                country="Romania",
                county="Bucuresti",
                city="Bucuresti",
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

    company_name = "Exiger"
    logo_link = "https://www.exiger.com/wp-content/uploads/2023/04/logo_midnight@2x.png.webp"

    jobs = scraper()
    print(len(jobs))
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
