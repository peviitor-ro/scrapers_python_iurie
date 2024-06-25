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
# Company ---> Computacenter
# Link ------> https://careers.computacenter.com/ro
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
    ... scrape data from Computacenter scraper.
    """
    job_list = []
    #extract job categories links
    soup = GetStaticSoup("https://careers.computacenter.com/ro")
    job_categories = soup.find_all("a", class_="item")
    for link in job_categories:
        category=link.get("href")
        #check if jobs are available per category
        job_category=GetStaticSoup(category)
        if  job_category.find_all("div",class_="moduleItems-items"):
            # extract job info 
            for job in job_category.find_all("a",class_="shont item"):

                # get jobs items from response
                job_list.append(Item(
                    job_title=job.find("div",class_="h3").text,
                    job_link=job.get("href"),
                    company="Computacenter",
                    country="România",
                    county="Cluj",
                    city="Cluj",
                    remote="remote",
                ).to_dict())
        else:
            continue

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Computacenter"
    logo_link = "https://careers.computacenter.com/ro/uploads/26b6f45b-d5aa-478d-9b59-c89355d9b7a3/settings/companies/computacenter-rou-eftl3-96-658061442d250.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
