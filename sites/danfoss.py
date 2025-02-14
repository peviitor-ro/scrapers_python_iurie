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
# Company ---> danfoss
# Link ------> https://jobs.danfoss.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&geolocation=&optionsFacetsDD_department=&optionsFacetsDD_facility=
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
    ... scrape data from danfoss scraper.
    """
    # link
    # https://jobs.danfoss.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&geolocation=&optionsFacetsDD_department=&optionsFacetsDD_facility=
    soup = GetStaticSoup(
        "https://jobs.danfoss.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&geolocation=&optionsFacetsDD_department=&optionsFacetsDD_facility="
    )

    job_list = []
    for job in soup.find_all("div", class_="jobdetail-phone visible-phone"):
        location = job.find("span", class_="jobLocation").text.strip().split(", RO")[0]
        location = "Bucuresti" if "Bucharest" in location else location
        job_title = job.find("a").text
        if job_title == "Cloud Architect (Infrastructure)":
            location = "Bucuresti"
        # get jobs items from response
        job_list.append(
            Item(
                job_title=job_title,
                job_link="https://jobs.danfoss.com" + job.find("a")["href"],
                company="danfoss",
                country="România",
                county=get_county_json(location),
                city=location,
                remote="remote",
            ).to_dict()
        )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "danfoss"
    logo_link = "https://www.danfoss.com/static/images/logo.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
