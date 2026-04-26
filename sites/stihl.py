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
# Company ---> stihl
# Link ------> https://www.stihl.ro/ro/informatii-utile/despre-noi/cariere-stihl-ro
#
#
from __utils import (
    Item,
    UpdateAPI,
)
import requests


def scraper():
    """
    ... scrape data from stihl scraper.
    """
    response = requests.get(
        "https://corporate.stihl.ro/content/corporate/ro/ro/career/job-offers.corporatejoblisting.json",
        params={"limit": 30, "offset": 0},
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
        timeout=30,
    )
    data = response.json()

    job_list = []
    for job in data.get("results", []):

        # get jobs items from response
        job_list.append(
            Item(
                job_title=job["jobTitle"],
                job_link="https://corporate.stihl.ro/ro/cariera/locuri-de-munca/detalii-job/"
                + str(job["jobId"]),
                company="stihl",
                country="România",
                county="Bihor",
                city="Oradea",
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

    company_name = "stihl"
    logo_link = "https://toppng.com/public/uploads/preview/stihl-company-vector-logo-11574273111d1t9lxqbv3.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
