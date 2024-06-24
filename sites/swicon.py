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
# Company ---> Swicon
# Link ------> https://swicon.com/ro/romania
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
    ... scrape data from Swicon scraper.
    """
    soup = GetStaticSoup("https://swicon.com/ro/romania")

    job_list = []
    for job in soup.find_all("div",class_="col-12 col-sm-6 col-md-4 col-lg-3"):
        print(job)

        # get jobs items from response
        job_list.append(Item(
            job_title="not finissed",
            job_link="",
            company="Swicon",
            country="România",
            county="",
            city="",
            remote="",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Swicon"
    logo_link = "logo_link"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    #UpdateAPI().publish(jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
