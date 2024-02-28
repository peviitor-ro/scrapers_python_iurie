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
# Company ---> ENGIE
# Link ------> https://jobs.engie.com/search/?q=&locationsearch=Romania
#
#
import time
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
    ... scrape data from ENGIE scraper.
    '''
    page = 0
    job_list = []
    locations =[]
    flag = True
    
    while flag:
        soup = GetStaticSoup(f"https://jobs.engie.com/search/?q=&locationsearch=Romania&startrow={page}")

        if len(data_soup := soup.find_all('tr', attrs=('data-row'))) >0:
            for job in data_soup:
                # Remove "Romania" from the location --- Start
                locations = job.find('span', attrs ='jobLocation').text.strip().split(', R')[0].split(', ')
                for loc in range(len(locations)):
                    if 'pi' in locations[loc].lower():
                        locations[loc] =  'Pitesti'# locations[loc].replace('Pi','Pitesti')
                    if 'COURBEVOIE'.lower() in locations[loc].lower():
                        locations = 'all'
                    

                print(locations)
            
                
                # get jobs items from response
                job_list.append(Item(
                    job_title=job.find('a', attrs='jobTitle-link').text,
                    job_link='https://jobs.engie.com'+ job.find('a')['href'],
                    company='Engie',
                    country='Romania',
                    county='',
                    city='',
                    remote='On-site',
                ).to_dict())
    
        else:
            flag = False
        
        # increment page
        page += 25
        time.sleep(1)
    
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Engie"
    logo_link = "https://rmkcdn.successfactors.com/c4851ec3/1960b45a-f47f-41a6-b1c7-c.svg"

    jobs = scraper()
    # print(jobs)
    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
