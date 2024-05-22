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
    for job in soup.find_all("div",attrs="views-row col-md-4"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("span", attrs="field field--name-title field--type-string field--label-hidden").text,
            job_link=job.find("a")["href"],
            company="Simavi",
            country="Romania",
            county = None,
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
    logo_link = "https://www.simavi.ro/sites/default/files/2018-07/logo-construction_0.png"
    start_time=time.time()
    jobs = scraper()
    end_time=time.time()
    
    print("jobs found:",len(jobs))
    print("execution time", round(end_time-start_time),"sec")
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
