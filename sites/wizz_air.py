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
# Company ---> Wizz Air
# Link ------> https://careers.wizzair.com/search/?locationsearch=Romania
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
    ... scrape data from Wizz Air scraper.
    """
    soup = GetStaticSoup("https://careers.wizzair.com/search/?locationsearch=Romania")

    job_list = []
    for job in soup.find_all("tr",class_="data-row"):
        location=job.find("span", class_="jobLocation").text.strip().split(",")[0]

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("a").text,
            job_link="https://careers.wizzair.com"+job.find("a")["href"],
            company="Wizz Air",
            country="România",
            county=get_county_json(location),
            city=location,
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Wizz Air"
    logo_link = "https://cdn0.scrvt.com/airportdtm/public/airportdtm/49dfd2e90d79c55b/12e3c120959a/v/f297642e71ca/wizzair-logo-web.jpg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
