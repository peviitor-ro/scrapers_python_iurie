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
    soup = GetStaticSoup("https://www.fntsoftware.com/en/careers/career-opportunities")

    job_list = []

    for job in soup.find('div', attrs=('link-liste')):
    
        print(job.find('a')['href'])
       
        # get jobs items from response
        job_list.append(Item(
            job_title = job.text.strip(),
            job_link = '',
            company = 'FntSoftware',
            country = 'Romania',
            county = '',
            city = '',
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
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
