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
# Company ---> Cognizant
# Link ------> https://careers.cognizant.com/global-en/jobs/?keyword=&location=Romania&lat=&lng=&cname=Romania&ccode=RO&origin=global
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
    ... scrape data from Cognizant scraper.
    """
    soup = GetStaticSoup("https://careers.cognizant.com/global-en/jobs/?keyword=&location=Romania&lat=&lng=&cname=Romania&ccode=RO&origin=global")

    job_list = []
    for job in soup.find_all("div",class_="card-body"):
        link="https://careers.cognizant.com"+job.find("a",class_="stretched-link js-view-job")["href"]
        #open job position and extarct job type from job page
        data_job = GetStaticSoup(link)
        job_type = data_job.find("div",class_="key-info").findAll("dd")[-1].text.strip()

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("a",class_="stretched-link js-view-job").text,
            job_link=link,
            company="Cognizant",
            country="România",
            county="Bucuresti",
            city="Bucuresti",
            remote=get_job_type(job_type),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Cognizant"
    logo_link = "https://careers.cognizant.com/images/logo.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
