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
# Company ---> Zenitech
# Link ------> https://zenitech.co.uk/careers/
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
    ... scrape data from Zenitech scraper.
    '''
    soup = GetStaticSoup("https://zenitech.co.uk/careers/")

    job_list = []
    for job in soup.find_all('div', attrs=('elementor-element elementor-element-2b13778 e-con-full e-flex e-con e-child')):
        
        #logic to extract location
        find_location =  job.find('div', attrs =('elementor-element-cca09fe'))
        if find_location:
            data_text = find_location.text
            
            if "Cluj-Napoca" in data_text:
                location_finish = get_county('Cluj-Napoca')
            #end location finis and get county
            
                # get jobs items from response
                job_list.append(Item(
                    job_title= job.find('h2').text,
                    job_link= job.find('a')['href'],
                    company='Zenitech',
                    country='Romania',
                    county=location_finish[0] if True in location_finish else None,
                    city='all' if True in location_finish and location_finish[0].lower() != 'bucuresti' else location_finish[0],
                    remote=get_job_type('Hybrid') if 'Hybrid' in data_text else get_job_type(''),
                ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Zenitech"
    logo_link = "https://zenitech.co.uk/wp-content/uploads/2020/11/Zenitech-logo-red.svg"

    jobs = scraper()
    # print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
