"""Config for Dynamic Get Method -> For Json format!

Company ---> Freudenberg Performance Materials SRL
Link ------> https://jobs.freudenberg.com/Freudenberg/?company=FPM&location=RO

"""

import json

import requests

from __utils import Item, UpdateAPI


API_URL = "https://r.jina.ai/https://jobs.freudenberg.com/Freudenberg/api/json/?company=FPM&location=L_00000038"
def _load_jobs():
    response = requests.get(API_URL, timeout=60)
    response.raise_for_status()
    text = response.text
    return json.loads(text[text.find("{"):])


def scraper():
    """
    ... scrape data from Freudenberg Performance Materials SRL scraper.
    """
    json_data = _load_jobs()

    job_list = []
    for job in json_data["jobs"]:
        job_list.append(
            Item(
                job_title=job["jobtitle"],
                job_link=job["deepLink"],
                company="Freudenberg Performance Materials SRL",
                country="Romania",
                county="Brasov",
                city="Brasov",
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

    company_name = "Freudenberg Performance Materials SRL"
    logo_link = "https://www.freudenberg-pm.com/-/media/Images/Logos/FREUDENBERG_PERFORMANCE_MATERIALS.svg?h=48&w=294&la=en&hash=ACFC54066D4BB1FDBDAA4826B6F4A294"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
