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
# Company ---> Voxility
# Link ------> https://www.voxility.com/jobs
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
    ... scrape data from Voxility scraper.
    '''
    base_link = "https://www.voxility.com/jobs" 
    soup = GetStaticSoup(base_link)

    job_list = []
    for job in soup.find_all('h4', attrs={'job-title'}):
        
        #check if job tipe contain in job title
        if 'hybrid' in job.find('a').text.lower():
           job_type = 'hybrid'
        elif 'remote' in job.find('a').text.lower():
            job_type = 'remote'
        else:
            job_type = 'On-site'
        
       #extrarct location from job_location and replace bucharest to Bucuresti
        if (location := job.find('span', attrs={'job-location'}).text.split()[-2].replace(',','').lower() in ['bucharest']):
            location = 'Bucuresti'
        else:
            location = None
        

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('a').text,
            job_link = base_link + job.find('a',)['href'].replace('..',''),
            company = 'Voxility',
            country = 'Romania',
            county = location if True in get_county(location)  else get_county(location)[0],
            city = location,
            remote = job_type,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Voxility"
    logo_link = "https://www.voxility.com/public/themes/mobile_VoxilityLogo.png"

    jobs = scraper()
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
