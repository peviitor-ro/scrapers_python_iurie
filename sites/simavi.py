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
# Company ---> Simavi
# Link ------> https://simavi.ro/cariere
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
import time

def scraper():
    """
    ... scrape data from Simavi scraper.
    """
    
    soup = GetStaticSoup("https://simavi.ro/cariere")

    job_list = []
    print(len(soup.find_all("div",attrs="views-row col-md-4")))
    for job in soup.find_all("div",attrs="views-row col-md-4"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("span", attrs="field field--name-title field--type-string field--label-hidden").text,
            job_link=job.find("a")["href"],
            company="Simavi",
            country="România",
            county = "București",
            city="București",
            remote="on-site",
        ).to_dict())

    return job_list

def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Simavi"
    logo_link = "https://simavi.ro/sites/default/files/logo-construction_0.png" 
    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
