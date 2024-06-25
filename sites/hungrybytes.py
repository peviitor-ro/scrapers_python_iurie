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
    GetStaticSoup,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
import requests
import re

def scraper():
    """
    scrape data from HungryBytes scraper.
    """
    # Step 1: Fetch the content from the URL
    url = "https://jobs.hungrybytes.co/_next/static/chunks/pages/index-3d23841ba24dc5b4.js"
    response = requests.get(url)
    content = response.text
    # Define regex patterns to extract titles and link and location
    title_pattern = re.compile(r'title:"(.*?)"')
    slug_pattern = re.compile(r'slug:"(.*?)"')
    location_pattern = re.compile(r'category:"(.*?)"')
    # Find all matches for titles and slugs
    titles=title_pattern.findall(content)[::2][:-1]
    slugs=slug_pattern.findall(content)
    # Filter and clean the locations list
    locations=location_pattern.findall(content)
    cleaned_locations = [location.replace(", Romania", "").strip() for location in locations if "ListJobs_category__NeNg1" not in location]
   
    job_list = []
    for title,link, city in zip(titles, slugs, cleaned_locations):
       
        # get jobs items from response
        job_list.append(Item(
            job_title=title,
            job_link="https://jobs.hungrybytes.co/careers/"+link+"/",
            company="HungryBytes",
            country="România",
            county="Iasi",
            city=city,
            remote=get_job_type(content),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "HungryBytes"
    logo_link = "https://assets.static-upwork.com/org-logo/1724096907641098240"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
