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
# Company ---> TecAlliance
# Link ------> https://career.tecalliance.net/jobs?country=Romania&split_view=true&query=
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
    ... scrape data from TecAlliance scraper.
    """
    soup = GetStaticSoup("https://career.tecalliance.net/jobs?country=Romania&split_view=true&query=")

    job_list = []
    jobs_class = "flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg focus-visible-company focus-visible:rounded"
    
    for job in soup.find_all("a", attrs=jobs_class):
        data = job.find("div", attrs="mt-1 text-md").text.strip()
        
        # get jobs items from response
        job_list.append(Item(
            job_title = job.find("span", attrs="text-block-base-link").text.strip(),
            job_link = job.get("href"),
            company = 'TecAlliance',
            country = 'România',
            county = "Gorj",      
            city = 'Dragoeni',
            remote = get_job_type(data),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "TecAlliance"
    logo_link = "https://www.brightlands.com/sites/default/files/styles/max_2600x2600/public/2022-02/BSSC%20TecAlliance%20Logo_rgb.jpg?itok=W3ir7dN8"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
