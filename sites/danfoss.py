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
# Company ---> danfoss
# Link ------> https://jobs.danfoss.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&geolocation=&optionsFacetsDD_department=&optionsFacetsDD_facility=
#
#
from __utils import (
    GetDataCurl,
    Item,
    UpdateAPI,
)

import re


def scraper():
    """
    ... scrape data from danfoss scraper.
    """
    search_text = GetDataCurl(
        "https://r.jina.ai/http://https://jobs.danfoss.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&geolocation=&optionsFacetsDD_department=&optionsFacetsDD_facility="
    )
    if not search_text:
        return []

    job_list = []
    jobs = re.findall(r"\*\s+\[(.*?)\]\((https://jobs\.danfoss\.com/job/[^\)]+)\)\s+(.*?)\s+Job Category", search_text)
    for job_title, job_link, location in jobs:
        if "multiple" in location.lower():
            city = "Bucuresti"
            county = "Bucuresti"
        else:
            city = "Bucuresti" if "Bucharest" in location else location.split(", RO")[0].strip()
            county = city

        job_list.append(
            Item(
                job_title=job_title,
                job_link=job_link,
                company="danfoss",
                country="Romania",
                county=county,
                city=city,
                remote="remote",
            ).to_dict()
        )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "danfoss"
    logo_link = "https://www.danfoss.com/static/images/logo.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
