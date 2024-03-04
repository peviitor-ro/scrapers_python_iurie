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
    city_loc =[]
    flag = True
    
    while flag:
        soup = GetStaticSoup(f"https://jobs.engie.com/search/?q=&locationsearch=Romania&startrow={page}")

        if len(jobs := soup.find_all('tr', attrs=('data-row'))) >0:
            for job in jobs:
                
                # Remove "Romania" from the location --- Start
                city_loc = job.find('span', attrs ='jobLocation').text.strip().title().split(', R')[0].split(', ')
                
                # Check if 'COURBEVOIE' exists in the list
                if 'COURBEVOIE'.title() in city_loc:
                    # Replace all elements with just 'all'
                    city_loc= ['all']
                    
                for loc in range(len(city_loc)):
                    if 'bucharest' in city_loc[loc].lower():
                        city_loc[loc] = 'Bucuresti'  
                    if 'pi' in city_loc[loc].lower():
                        city_loc[loc] =  'Pitesti'
                    if 'crai' in city_loc[loc].lower() or 'Craiova' in city_loc[loc].lower():
                        city_loc[loc] =  'Craiova'
                        
                # check county for cities from city_loc list   
                job_county =[get_county(city) for city in city_loc]
                # try to find if city is a county if yes add to a list county if not then non
                get_county_if_city_is_county = [city[0] if True in city else None for city in job_county]
                
                city_all = 'all' if not None in get_county_if_city_is_county and get_county_if_city_is_county[0].lower() != 'bucuresti' else city_loc 
                
                # get jobs items from response
                job_list.append(Item(
                    job_title=job.find('a', attrs='jobTitle-link').text,
                    job_link='https://jobs.engie.com'+ job.find('a')['href'],
                    company='Engie',
                    country='Romania',
                    county= get_county_if_city_is_county if not None in get_county_if_city_is_county else None,
                    city= city_all if len(city_loc)==1 else 'all',
                    # for location if all then location remote else On-site
                    remote= get_job_type(''),
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
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
