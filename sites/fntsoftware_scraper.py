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
# Company ---> FntSoftware
# Link ------> https://www.fntsoftware.com/en/careers/career-opportunities
#
#
from bs4 import BeautifulSoup
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    """
    ... scrape data from FntSoftware scraper.
    """
    job_list = []
    soup = GetStaticSoup("https://www.fntsoftware.com/en/careers/career-opportunities")
    
    #find div element from page and save it in a string 
    data = str(soup.find('div', attrs=('link-liste')))
    #parese on emore time data string to a soup to be able to iterate and extract job data
    soup_jobs = BeautifulSoup(data, 'lxml')
    jobs = soup_jobs.find_all('a')

    
    for job in jobs:
        link = f"https://www.fntsoftware.com/{job.get('href')}"
        title = job.find('span', class_='link-liste__text').text
        
        # get jobs items from response
        job_list.append(Item(
            job_title = title,
            job_link = link,
            company = 'FntSoftware',
            country = 'Romania',
            county = None,
            city = 'Timisoara',
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "FntSoftware"
    logo_link = "https://fntsoftware.com/blog/wp-content/uploads/2023/09/FNT-Logo_simplify-complexity_RGB.png"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
