"""

 Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> Zonkwave
Link ------> https://zonkwave.com/careers/

"""
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Zonkwave scraper.
    """
    soup = GetStaticSoup("https://zonkwave.com/careers/")

    job_list = []
    for job in soup.find_all("div",class_="job-content"):

        job_details = job.find("div", class_="job-details").text.strip()

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h4").text,
            job_link=job.find("a").get("href"),
            company="zonkwave",
            country="România",
            county="București",
            city="București",
            remote=get_job_type(job_details),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "zonkwave"
    logo_link = "https://zonkwave.com/wp-content/uploads/2024/12/Logo-ZONKWAVE-landscape-1.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
