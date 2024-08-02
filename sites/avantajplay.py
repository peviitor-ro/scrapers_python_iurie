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
# Company ---> AvantajPlay
# Link ------> https://www.avantajplay.ro/vacancies/
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
    ... scrape data from AvantajPlay scraper.
    """
    soup = GetStaticSoup("https://www.avantajplay.ro/vacancies/")

    job_list = []
    for job in soup.find_all('div', attrs = ('b-vacancies__item')):
        
        county = get_county('București')
        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h2' , attrs = ('b-vacancies__title')).text,
            job_link = job.find('a' , attrs = ('b-vacancies__link'))['href'],
            company = 'Avantajplay',
            country = 'România',
            county = county[0] if True in county else None,
            city = 'all' if True in county and county[0] != 'Bucuresti' else county[0],
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Avantajplay"
    logo_link = "https://www.avantajplay.ro/wp-content/uploads/2015/07/logo.png"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
