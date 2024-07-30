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
# Company ---> Codezilla
# Link ------> https://codezilla.global/jobs
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


'''
    ########################################################################
'''


def scraper():
    '''
    ... scrape data from Codezilla scraper.
    '''
    soup = GetStaticSoup("https://codezilla.global/jobs")

    job_list = []
    
    
        
    for job in soup.find_all('div', attrs='JobListing_certified_inner__naKv8 certified'):
        title=job.find('h3').text
        if title == "Business Development Manager":
            location="București"
        else:
            location = ['București','Iași']   
        # get jobs items from response  
        job_list.append(Item(
            job_title= title,
            job_link='https://codezilla.global'+job.find('a')['href'],
            company='Codezilla',
            country='România',
            county = location,
            city=location,
            remote = "on-site",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Codezilla"
    logo_link = "https://api.codezilla.ro/uploads/logo_black_03bc39c300.png"

    jobs = scraper()
    print(len(jobs))

    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
