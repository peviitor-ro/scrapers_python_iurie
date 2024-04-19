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
# Company ---> Sampamind
# Link ------> https://www.sampamind.com/jobs
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
    '''
    ... scrape data from Sampamind scraper.
    '''
    soup = GetStaticSoup("https://www.sampamind.com/jobs")
   
   
    job_list = []
    for job in soup.find_all('a', attrs={'text-decoration-none'}):
    
        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h3', attrs = {'class':'text-secondary mt0 mb4'}).text.strip(),
            job_link ='https://www.sampamind.com'+job.get('href'),
            company ='Sampamind',
            country  ='România',
            county = None, #"București" if True in  get_county('București')  else None,
            city = 'București',
            remote = get_job_type(''),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Sampamind"
    logo_link = "https://www.sampamind.com/web/image/website/1/logo/Sampa%20Mind?unique=ea61a00"

    jobs = scraper()

    # # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
