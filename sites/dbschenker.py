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
# Company ---> dbschenker
# Link ------> https://www.dbschenker.com/global/careers/jobs-portal?query=&formState=W3siY291bnRyeUlkIjpbIlJPIl19XQ%3D%3D
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
    ... scrape data from dbschenker scraper.
    https://www.dbschenker.com/global/careers/jobs-portal?query=&location=romania
    """
    soup = GetStaticSoup(
        "https://www.dbschenker.com/global/careers/jobs-portal?query=&formState=W3siY291bnRyeUlkIjpbIlJPIl19XQ%3D%3D")

    job_list = []
    for job in soup.find_all("article", class_="result"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h2", class_="h6-font-id result__title").text,
            job_link="https://www.dbschenker.com"+job.find("a").get("href"),
            company="DB schenker",
            country="România",
            county="București",
            city="București",
            remote=["hybrid", "remote"],
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "DB schenker"
    logo_link = "https://www.logolynx.com/images/logolynx/c0/c0a0ce74d26aa6a69f31c027de4949e2.jpeg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
