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
# Company ---> hirschmann-automotive
# Link ------> https://career.hirschmann-automotive.com/en/all-jobs?tx_site_jobapi%5Bcontroller%5D=Job&type=1598607815
#
#
from __utils import (
    get_county_json,
    Item,
    UpdateAPI,
)
import requests
from bs4 import BeautifulSoup


def scraper():
    """
    ... scrape data from hirschmann-automotive scraper.
    https://career.hirschmann-automotive.com/en/all-jobs
    """
    url = "https://career.hirschmann-automotive.com/en/all-jobs"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    data = BeautifulSoup(response.text, "html.parser")

    job_list = []
    for job in data.select("ul.jobs-list > li"):
        link_tag = job.find("a", href=True)
        title_tag = job.find("h3")
        if not link_tag or not title_tag:
            continue

        location_text = job.get_text(" ", strip=True)
        if "Romania" not in location_text:
            continue

        city = "Targu Mures"

        # get jobs items from response
        county = get_county_json(city)
        job_list.append(Item(
            job_title=title_tag.get_text(strip=True),
            job_link="https://career.hirschmann-automotive.com" +
            link_tag.get("href"),
            company="hirschmann automotive",
            country="România",
            county=county[0] if isinstance(county, list) else county,
            city=city,
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "hirschmann automotive"
    logo_link = "https://www.aki-gmbh.com/wp-content/uploads/logo-hirschmann-automotive.jpg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
