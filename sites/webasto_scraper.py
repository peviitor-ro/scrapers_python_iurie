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
# Company ---> Webasto
# Link ------> https://jobs.webasto.com/search/?q=&q2=&alertId=&title=&location=RO&shifttype=&date=&department=
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
    ... scrape data from Webasto scraper.
    """
    soup = GetStaticSoup("https://jobs.webasto.com/search/?q=&q2=&alertId=&title=&location=RO&shifttype=&date=&department=")

    job_list = []
    for job in soup.find_all('tr', attrs=('data-row')):
       
        location = job.find('span', attrs = ('jobLocation')).text.strip().split(', R')[0]
        county = get_county(location)
        
        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('a', attrs = ('jobTitle-link')).text,
            job_link = 'https://jobs.webasto.com/'+job.find('a', attrs = ('jobTitle-link'))['href'],
            company = 'Webasto',
            country = 'Romania',
            county = county[0] if True in county else None,
            city = 'all' if True in county and county  !='Bucuresti' else location ,
            remote =  get_job_type(''),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Webasto"
    logo_link = "https://logodix.com/logo/1699232.png"

    jobs = scraper()
    # print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
