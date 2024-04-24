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
# Company ---> Foundever
# Link ------> https://jobs.foundever.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_title=&optionsFacetsDD_country=&optionsFacetsDD_department=
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Foundever scraper.
    """
    soup = GetStaticSoup("https://jobs.foundever.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_title=&optionsFacetsDD_country=&optionsFacetsDD_department=")

    job_list = []
    base_link = "https://jobs.foundever.com"
    
    for job in soup.find_all("tr",attrs="data-row"):
        
        job_data = job.find("span", attrs="jobLocation").text.strip()
        # get jobs items from response
        job_list.append(Item(
            job_title = job.find("a").text,
            job_link = base_link + job.find("a")["href"],
            company="Foundever",
            country="Romania",
            county = None,
            city = "all",
            remote = get_job_type(job_data),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Foundever"
    logo_link = "https://rmkcdn.successfactors.com/1698e3f5/b7ce9b2f-1001-490c-add1-3.svg"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
