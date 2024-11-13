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
    soup = GetStaticSoup("https://zenitech.co.uk/careers/romania/")

    job_list = []
    
    for job in soup.find_all('div', class_=('elementor-element elementor-element-2b13778 e-con-full e-flex e-con e-child')):
        
        #job data
        data = job.find('div', class_ =('elementor-element-cca09fe')).text.strip()
        
        if "Romania" in data:
            job_type = get_job_type(data)
                
            #get jobs items from response
            job_list.append(Item(
                job_title = job.find('h2').text,
                job_link = job.find('a')['href'],
                company='Zenitech',
                country='România',
                county = "Cluj",
                city='Cluj-Napoca',
                remote = job_type,
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
    print("Found jobs",len(jobs))
    # print(jobs)
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
