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
# Company ---> Esolution
# Link ------> https://www.esolutions.tech/careers
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
    ... scrape data from Esolution scraper.
    """
    soup = GetStaticSoup("https://www.esolutions.tech/careers")

    job_list = []
    for job in soup.find_all("div",class_="careers-wrapper mb-3"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h3").text.strip(),
            job_link="https://www.esolutions.tech"+job.find("a", class_="primary-button")["href"],
            company="Esolution",
            country="România",
            county="București",
            city="București",
            remote=job.find("a", class_="job-tag").text.lower(),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Esolution"
    logo_link = "https://www.esolutions.tech/icons/esol.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
