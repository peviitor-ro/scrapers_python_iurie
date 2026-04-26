#
#
#  Basic for scraping data from static pages
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> Swicon
# Link ------> https://swicon.com/jobs
#
#
from __utils import (
    Item,
    UpdateAPI,
)
from html import unescape
import json
import re
import subprocess


def get_jobs_feed():
    payload = subprocess.check_output(
        [
            "curl",
            "-L",
            "-s",
            "https://swicon-jobs.com/wp-json/wp/v2/swiconjobad?categories=8&per_page=100",
        ],
        text=True,
    )
    return json.loads(payload)


def scraper():
    """
    ... scrape data from Swicon scraper.
    """
    jobs = get_jobs_feed()

    job_list = []
    for job in jobs:
        content = job.get("content", {}).get("rendered", "")
        lowered_content = content.lower()
        if "no longer available" in lowered_content or "not yet available" in lowered_content:
            continue

        match = re.search(r"<p>\s*([^|<]+?)\s*\|\s*([^<]+?)\s*</p>", content, re.I)
        if not match:
            continue

        city = match.group(1).strip()
        remote = match.group(2).strip().lower()
        if city != "Bucharest":
            continue

        job_list.append(
            Item(
                job_title=unescape(job["title"]["rendered"]),
                job_link=job["link"],
                company="Swicon",
                country="România",
                county="Bucuresti",
                city="Bucuresti",
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

    company_name = "Swicon"
    logo_link = "https://www.ejobs.ro/img/userCoverPhoto/f/5/f5e56fe04b0618594c10407feb11ecd4.jpg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
