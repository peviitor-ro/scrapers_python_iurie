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
# Company ---> Grab
# Link ------> https://www.grab.careers/en/jobs/?search=&country=Romania&pagesize=20#results
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
    ... scrape data from Grab scraper.
    """
    soup = GetStaticSoup("https://www.grab.careers/en/jobs/?search=&country=Romania&pagesize=20#results")
    
    job_list = []
    for job in soup.find_all("div",class_="card-body"):
    
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h2",class_="card-title").text,
            job_link="https://www.grab.careers"+job.find("a",class_="stretched-link js-view-job")["href"],
            company="Grab",
            country="România",
            county="Cluj",
            city=job.find("li",class_="list-inline-item").text.strip().split(", R")[0],
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Grab"
    logo_link = "https://www.grab.careers/images/logo.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
