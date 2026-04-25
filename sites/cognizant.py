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
# Company ---> Cognizant
# Link ------> https://careers.cognizant.com/global-en/jobs/?keyword=&location=Romania&lat=&lng=&cname=Romania&ccode=RO&origin=global
#
#
import re

from __utils import GetDataCurl, Item, UpdateAPI, get_job_type


LISTING_URL = "https://r.jina.ai/http://https://careers.cognizant.com/global-en/jobs/?keyword=&location=Romania&lat=&lng=&cname=Romania&ccode=RO&origin=global"


def scraper():
    """
    ... scrape data from Cognizant scraper.
    """
    listing_text = GetDataCurl(LISTING_URL)
    if not listing_text:
        return []

    job_list = []
    jobs = re.findall(
        r"## \[(.*?)\]\((https://careers\.cognizant\.com/[^\)]+)\)\s+Save Saved\s+\*\s+(.*?)\s+\*\s+(.*?)\s",
        listing_text,
        re.S,
    )
    for title, link, location, _department in jobs:
        if "romania" not in location.lower():
            continue

        detail_text = GetDataCurl(f"https://r.jina.ai/http://{link}")
        job_type = "on-site"
        if detail_text:
            if "work from office" in detail_text.lower():
                job_type = "on-site"
            elif "hybrid" in detail_text.lower():
                job_type = "hybrid"
            elif "remote" in detail_text.lower():
                job_type = "remote"

        # get jobs items from response
        job_list.append(Item(
            job_title=title.strip(),
            job_link=link,
            company="Cognizant",
            country="Romania",
            county="Bucuresti",
            city="Bucuresti",
            remote=get_job_type(job_type),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Cognizant"
    logo_link = "https://careers.cognizant.com/images/logo.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
