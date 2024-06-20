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
# Company ---> Deloitte
# Link ------> https://apply.deloittece.com/en_US/careers/SearchJobs/?523=%5B5509%5D&523_format=1482&listFilterMode=1&jobRecordsPerPage=10&jobOffset=0
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
import time

def scraper():
    """
    ... scrape data from Deloitte scraper.
    """
    job_list = []
    location = []
    page = 0
    flag = True
    
    while flag:
        soup = GetStaticSoup(f"https://apply.deloittece.com/en_US/careers/SearchJobs/?523=%5B5509%5D&523_format=1482&listFilterMode=1&jobRecordsPerPage=10&jobOffset={page}")
        if len(jobs := soup.find_all('div', attrs=('article__header__text'))) > 1:
            
            for job in jobs:
                # print(job.find('div', attrs = ('article__header__text__subtitle')).text.strip())
                # data = ' '.join(span.text.strip() for span in job.find_all('span'))
                span_elements = job.find_all('span')
                #extract data from span elements location and job type 
                job_type_data = span_elements[-1].text.strip()
                location_data = span_elements[0].text.strip().split('- R')[0].replace(',', '')
                #check if Bucharest and replace it with Bucuresti
                if 'Bucharest' in location_data:
                    location_data = location_data.replace('Bucharest','București')
                location = location_data.split()
                #create a list only  if location is county 
                check_county = [county for county in location if True in get_county(county)]
               
                # get jobs items from respons
                job_list.append(Item(
                    job_title = job.find('a').text.strip(),
                    job_link = job.find('a')['href'],
                    company = 'Deloitte',
                    country = 'România',
                    county = check_county,
                    city = 'all' if len(check_county) == len(location) and check_county[0]!='București' else location,
                    remote = get_job_type(job_type_data),
                ).to_dict())
        else:
            flag = False
            break
        # increment page
        page += 10
        time.sleep(1)
    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Deloitte"
    logo_link = "https://www.bher.ca/sites/default/files/images/2022-03/Deloitte-Logo.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
