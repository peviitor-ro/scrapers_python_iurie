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
# Company ---> Interra
# Link ------> https://www.interra.ro/angajari/
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Interra scraper.
    """
    soup = GetStaticSoup("https://www.interra.ro/angajari/")

    job_list = []
    for job in soup.find_all("div",attrs="col-md-7 col-lg-8 align-self-center"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text,
            job_link = job.find('a')["href"],
            company="Interra Travel",
            country="România",
            county="București",
            city = "București",
            remote = "on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "InterraTravel"
    logo_link = "https://www.interra.ro/img/main-logo.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':  
    main()
