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
# Company ---> Exiger
# Link ------> https://www.exiger.com/careers/
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
    ... scrape data from Ezugi scraper.
    '''
    soup = GetStaticSoup("https://careers.ezugi.com/jobs?split_view=true&query=")
    job_list = []
    
    for job in soup.find_all('li', attrs=('w-full')):
        
        # job title
        title = job.find('span', attrs =('text-block-base-link sm:min-w-[25%] sm:truncate company-link-style')).text
       
        # find city
        data = job.find('div', attrs =('mt-1 text-md')).text.strip()
        location = list(data.split())
        loc = [word for word in location if word.lower() == 'bucharest'] #remove all elements exept buharest 
        # replace bucharest with Bucuresti in loc list 
        for word in range(len(loc)):
            if  loc[word].lower().strip() == 'bucharest':
                loc_f='București'
                
         # call func get_county to return tuple
        finish_location = get_county(location=loc_f)   
        #check job type from tytle and data 
        job_type = get_job_type(title + data)
        # get jobs items from response
        job_list.append(Item(
            job_title = title,
            
            job_link = job.find('a')['href'],
            company='Ezugi',
            country='Romania',
            county = None, 
            city='all' if True  in finish_location and 'remote' in job_type and finish_location[0] != 'Bucuresti' else finish_location[0],
            remote = job_type ,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Ezugi"
    logo_link = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/34b2d2c3-89da-4697-a57c-78cabbc1d793/original.png"

    jobs = scraper()
   
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
