"""
Basic for scraping data from static pages.

Company ---> Gameloft
Link ------> https://api.smartrecruiters.com/v1/companies/Gameloft/postings?limit=100&offset=0
"""

import requests

from __utils import Item, UpdateAPI


API_URL = "https://api.smartrecruiters.com/v1/companies/Gameloft/postings?limit=100&offset=0"


def scraper():
    """
    ... scrape data from Gameloft scraper.
    """
    json_data = requests.get(API_URL, timeout=30).json()

    job_list = []
    seen_refs = set()
    for job in json_data.get("content", []):
        location = job.get("location", {})
        if location.get("country") != "ro":
            continue

        ref_number = job.get("refNumber")
        if ref_number in seen_refs:
            continue
        seen_refs.add(ref_number)

        remote = "hybrid" if location.get("hybrid") else "remote" if location.get("remote") else "on-site"

        job_list.append(
            Item(
                job_title=job.get("name", "").strip(),
                job_link=f"https://jobs.smartrecruiters.com/Gameloft/{job.get('id')}",
                company="Gameloft",
                country="Romania",
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

    company_name = "Gameloft"
    logo_link = "https://www.gameloft.ro/wp-content/uploads/2017/05/logo_gameloft_black.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
