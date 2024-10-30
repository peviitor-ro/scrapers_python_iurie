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
# Company ---> stihl
# Link ------> https://www.stihl.ro/ro/informatii-utile/despre-noi/cariere-stihl-ro
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


def scraper():
    """
    ... scrape data from stihl scraper.
    """
    soup = GetStaticSoup("https://www.stihl.ro/ro/informatii-utile/despre-noi/cariere-stihl-ro")

    job_list = []
    for job in soup.find_all("div",class_="richtexteditor text"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h2").text.title(),
            job_link="https://www.stihl.ro"+job.find("a")["href"],
            company="stihl",
            country="România",
            county="Ilfov",
            city="Otopeni",
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "stihl"
    logo_link = "https://toppng.com/public/uploads/preview/stihl-company-vector-logo-11574273111d1t9lxqbv3.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
