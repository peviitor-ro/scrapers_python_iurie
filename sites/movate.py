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
# Company ---> Movate
# Link ------> https://www.movate.com/careers/job-listing-explore-career-openings-at-movate/?search_keywords=&selected_location=romania&selected_job_level=-1
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
    ... scrape data from Movate scraper.
    """
    soup = GetStaticSoup("https://www.movate.com/careers/job-listing-explore-career-openings-at-movate/?search_keywords=&selected_location=romania&selected_job_level=-1")

    job_list = []
    for job in soup.find_all("div",class_="list-data"):


        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("div", class_="job-info").text.strip(),
            job_link=job.find("div", class_="job-info").find("a")["href"],
            company="Movate",
            country="România",
            county="Bucuresti",
            city="Bucuresti",
            remote="remote",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Movate"
    logo_link = "https://movate-website-data.s3.ap-south-1.amazonaws.com/wp-content/uploads/2024/09/19091328/Movate-Logo-R-1.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
