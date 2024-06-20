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
# Company ---> TradeVille
# Link ------> https://tradeville.ro/cariere
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
    ... scrape data from TradeVille scraper.
    """
    soup = GetStaticSoup("https://tradeville.ro/cariere")

    job_list = []
    for job in soup.find_all("div",class_="accordion-item"):
        location=job.find("h2", class_="accordion-header").text.strip().split(", ")[1]
        job_description=job.find("div", class_="accordion-body").text
        print(job.find("h2", class_="accordion-header").text.strip().split(", ")[0])
       

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h2", class_="accordion-header").text.strip().split(", ")[0],
            job_link="",
            company="TradeVille",
            country="România", 
            county=get_county_json(location),
            city=location,
            remote=get_job_type(job_description),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "TradeVille"
    logo_link = "https://www.piatafinanciara.ro/wp-content/uploads/2017/04/tradeville.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    #UpdateAPI().publish(jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
