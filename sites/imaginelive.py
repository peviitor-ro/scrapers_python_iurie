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
# Company ---> imaginelive
# Link ------> https://career.imaginelive.com/en/vacancies
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
    ... scrape data from imaginelive scraper.
    """
    soup = GetStaticSoup("https://career.imaginelive.com/en/vacancies")

    job_list = []
    for job in soup.find_all("tr"):
        location = job.find(
            "div", class_="vacancies__text text-xs location-data search-data").text
        if "Romania" in location:
            city = "Bucuresti" if "Bucharest" in location else location.split(", R")[
                0]

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find(
                    "div", class_="vacancies__position search-data title-sm").text,
                job_link="https://career.imaginelive.com" +
                job.find("a").get("href"),
                company="imaginelive",
                country="România",
                county=get_county_json(city),
                city=city,
                remote="on-site",
            ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "imaginelive"
    logo_link = "https://career.imaginelive.com/assets/img/life-at-imaginelive.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
