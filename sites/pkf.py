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
# Company ---> PKF
# Link ------> https://pkffinconta.ro/cariere/
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
    ... scrape data from PKF scraper.
    """
    soup = GetStaticSoup("https://pkffinconta.ro/cariere/")

    job_list = []
    for job in soup.find_all("div",class_="vc_column_container col-md-4"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h3", class_="porto-sicon-title").text,
            job_link=job.find("a", class_="porto-sicon-box-link")["href"],
            company="PKF",
            country="România",
            county="Bucuresti",
            city="Bucuresti",
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "PKF"
    logo_link = "https://pkffinconta.ro/wp-content/uploads/2023/03/logo-web-2023.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
