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
# Company ---> Computacenter
# Link ------> https://careers.computacenter.com/ro
#
#
from __utils import (
    GetDataCurl,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)

import re


SEARCH_URL = "https://r.jina.ai/http://https://careers.computacenter.com/ro/search?utm_source=computacenter-ro&utm_medium=organic&utm_campaign=computacenter-ro"


def scraper():
    """
    ... scrape data from Computacenter scraper.
    """
    job_list = []
    search_text = GetDataCurl(SEARCH_URL)
    if not search_text:
        return job_list

    jobs = re.findall(
        r"### \[(.*?)\]\((https://careers\.computacenter\.com/ro/offer-redirect/[^\)]+)\)",
        search_text,
    )
    for title_with_meta, link in jobs:
        match = re.match(r"^(.*?)\s+(Cluj-Napoca|nationwide)\s+\*\s+.*$", title_with_meta.strip())
        if not match:
            continue

        title = match.group(1).strip()
        location = match.group(2).strip()

        if location.lower() == "nationwide":
            city = "all"
            county = "all"
            remote = "remote"
        else:
            city = location.split(", ")[-1]
            county = get_county_json(city)
            remote = "on-site"

        job_list.append(Item(
            job_title=title,
            job_link=link,
            company="Computacenter",
            country="Romania",
            county=county,
            city=city,
            remote=remote,
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Computacenter"
    logo_link = "https://cdn.job-shop.com/uploads/computacenter-6d1b97/WGGaZkTEQVYNIVaZfbTnaNLo.png?format=webp"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
