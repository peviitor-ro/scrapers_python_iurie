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
    #check if location is county
    location = ['București','Iași']
    county_finis = []
    for county in location: 
        county_finis.append(county if True in get_county(county) else None ) #if is county then append to a list 
        
   
    for job in soup.find_all('div', attrs='JobListing_certified_inner__naKv8 certified'):

        # get jobs items from response  
        job_list.append(Item(
            job_title= job.find('h3').text,
            job_link='https://codezilla.global'+job.find('a')['href'],
            company='Codezilla',
            country='Romania',
            county = county_finis,
            city='all' if True in county_finis or county_finis[0].lower()!='bucuresti' else None,
            remote = get_job_type(''),
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
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
