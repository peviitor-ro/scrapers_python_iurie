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
# Company ---> HungryBytes
# Link ------> https://jobs.hungrybytes.co/_next/static/chunks/pages/index-3d23841ba24dc5b4.js
#
#
from __utils import (
    Item,
    UpdateAPI,
)
import requests
import re

def scraper():
    """
    scrape data from HungryBytes scraper.
    """
    page = requests.get("https://jobs.hungrybytes.co", timeout=30)
    chunk_path = re.search(r'/_next/static/chunks/pages/index-[^.]+\.js', page.text).group(0)
    content = requests.get("https://jobs.hungrybytes.co" + chunk_path, timeout=30).text

    pattern = re.compile(
        r'title:"(?P<title>[^"]+)",slug:"(?P<slug>[^"]+)",category:"(?P<category>[^"]+)"'
    )

    job_list = []
    for match in pattern.finditer(content):
        title = match.group("title")
        slug = match.group("slug")
        city = match.group("category").replace(", Romania", "").strip()

        job_list.append(
            Item(
                job_title=title,
                job_link="https://jobs.hungrybytes.co/careers/" + slug + "/",
                company="Hungrybytes",
                country="România",
                county="Iasi",
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

    company_name = "Hungrybytes"
    logo_link = "https://assets.static-upwork.com/org-logo/1724096907641098240"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
