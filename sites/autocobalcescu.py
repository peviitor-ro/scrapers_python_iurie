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
# Company ---> autocobalcescu
# Link ------> https://www.autocobalcescu.ro/hr
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
    ... scrape data from autocobalcescu scraper.
    """
    soup = GetStaticSoup("https://www.autocobalcescu.ro/hr")

    job_list = []
    for job in soup.find_all("div", class_="card template-description"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h6").text.strip(),
            job_link=job.find("a")["href"],
            company="autocobalcescu",
            country="România",
            county="București",
            city="București",
            remote="",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "autocobalcescu"
    logo_link = "https://www.autocobalcescu.ro/images/logo.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
