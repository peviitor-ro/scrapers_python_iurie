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
# Company ---> Seimaf
# Link ------> https://www.seimaf.com/ro/ofertele-de-locuri-de-munca/?fwp_job_location=bucuresti-romania
#
# Jobs are loaded dynamically, so we use the public WP REST API
# filtered by the "bucuresti-romania" location term.

#
#
import html

import requests
import urllib3

from __utils import (
    Item,
    UpdateAPI,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "https://www.seimaf.com/wp-json/wp/v2/jobs"
LOCATION_ID = 646  # bucuresti-romania


def _fetch_jobs():
    params = {
        "job-locations": LOCATION_ID,
        "per_page": 100,
    }
    for _ in range(3):
        try:
            response = requests.get(
                API_URL,
                params=params,
                verify=False,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            continue
    return []


def scraper():
    """
    ... scrape data from Seimaf scraper.
    """
    job_list = []

    for job in _fetch_jobs():

        # get jobs items from response
        job_list.append(Item(
            job_title=html.unescape(job["title"]["rendered"]).strip(),
            job_link=job["link"],
            company="Seimaf",
            country="România",
            county="Bucuresti",
            city="Bucuresti",
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Seimaf"
    logo_link = "https://media.licdn.com/dms/image/C4D0BAQFBr5eOnAWpow/company-logo_200_200/0/1560859334430?e=2147483647&v=beta&t=bSgsiVGvV41-VRZZ_zPDuyQYq6BY0HfkG1w2eQ8SOcc"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
