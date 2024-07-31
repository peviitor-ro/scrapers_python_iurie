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
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from ENGIE scraper.
    '''
    page = 0
    flag = True
    job_list = []
    
    while flag:
        soup = GetStaticSoup(f"https://jobs.engie.com/search/?q=&locationsearch=Romania&startrow={page}")
        # print(soup)
        if len(jobs := soup.find_all('tr', attrs=('data-row'))) >0:
            for job in jobs:
            
                # Remove "Romania" from the location --- Start
                city_location = job.find('span', attrs ='jobLocation').text.strip().title().split(', R')[0].split(', ')
    
                # corect location typo    
                for city in range(len(city_location)):
                    
                    if 'Com.Blejoi' in city_location[city]:
                        city_location[city]='Blejoi'
                    if 'Bucharest' in city_location[city]:
                        city_location[city]='Bucuresti'
                    if 'Ploiest' in city_location[city]:
                        city_location[city] = 'Ploiesti'
                    if 'Turnu Mag' in  city_location[city]:
                        city_location[city] = 'Turnu Magurele'
                    if "Targu Mures" in city_location[city]:
                        city_location[city]="Targu-Mures"
              
                # check county for cities from city_loc list  add to a county list if True else not then None 
                job_county = [get_county_json(city)[0] for city in city_location]
                
                # get jobs items from response
                job_list.append(Item(
                    job_title = job.find('a', attrs='jobTitle-link').text,
                    job_link='https://jobs.engie.com'+ job.find('a')['href'],
                    company='ENGIE',
                    country='România',
                    county = job_county,
                    city = city_location,
                    # for location if all then location remote else On-site
                    remote = "on-site",
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

    company_name = "ENGIE"
    logo_link = "https://rmkcdn.successfactors.com/c4851ec3/1960b45a-f47f-41a6-b1c7-c.svg"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
