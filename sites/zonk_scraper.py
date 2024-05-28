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
# Company ---> ZONK
# Link ------> https://zonk.ro/cariere/
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
    ... scrape data from ZONK scraper.
    """
    soup = GetStaticSoup("https://zonk.ro/cariere/")

    job_list = []
    for job in soup.find_all("li",attrs="nav-item"):
        
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("a").text,
            job_link="https://zonk.ro/cariere/"+job.find("a")["href"],
            company="ZONK",
            country="România",
            county="București",
            city="București",
            remote=get_job_type("Hibrid"),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "ZONK"
    logo_link = "https://zonk.ro/wp-content/uploads/2023/09/logo-zonk-color-2023.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
