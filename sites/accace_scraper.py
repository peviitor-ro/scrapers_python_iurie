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
# Company ---> Accace
# Link ------> https://accace.ro/cariere/#oportunitati
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
    ... scrape data from Accace scraper.
    '''
    soup = GetStaticSoup("https://accace.ro/cariere/#oportunitati")

    job_list = []
    data_loc_type = []
    
    for job in soup.find_all('div',  attrs = ('col-md-4 col-sm-6 grid-item')):
        
        title = job.find('span', attrs = ('job-title')).text.strip()
        # Extract location and job type from page
        data_loc_type = job.find('div', attrs = ('job-location')).text.split(', ')
            
        if 'Bucuresti' in data_loc_type:
            finish_location = get_county(location ='Bucuresti' ) #get location finish with Bucuresti if Bucuresti is present in data_loc_type
        else:
            #if Bucuresti not in data_loc_type list get tuple with false to for county check
            finish_location = get_county('')    
           
            # get jobs items from response
        job_list.append(Item(
            job_title = title,
            job_link = job.find('a')['href'],
            company='Accace',
            country='Romania',
            county = None,
            city =  'all' if True in finish_location and finish_location[0].lower() != 'bucuresti' else finish_location[0],
            remote = get_job_type('hibrid') if title == 'Payroll Specialist' else get_job_type(job.find('div', attrs = ('job-location')).text),
        ).to_dict()) 

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Accace"
    logo_link = "https://www.movexstehovani.cz/wp-content/uploads/2018/09/LOGO_ACCACE_blue.png"

    jobs = scraper()
    print(len(jobs))
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
