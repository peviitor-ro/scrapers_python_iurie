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
# Company ---> Windsoft
# Link ------> https://www.windsoft.ro/ro/cariere
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
    ... scrape data from Windsoft scraper.
    """
    soup = GetStaticSoup("https://www.windsoft.ro/ro/cariere")

    job_list = []
    for job in soup.find_all("div",class_="col-xs-12 col-sm-6 col-md-4 col-lg-4 mv-20"):
        location=job.find("div",class_="career_location").text.capitalize()
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("a").text,
            job_link="https://www.windsoft.ro/"+job.find("a")["href"],
            company="Windsoft",
            country="România",
            county=get_county_json(location),
            city=location,
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Windsoft"
    logo_link = "https://www.windsoft.ro/images/logo.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
