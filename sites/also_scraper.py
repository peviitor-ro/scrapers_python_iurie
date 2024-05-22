#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> ALSO
# Link ------> https://www.also.com/ec/cms5/en_6000/6000/company/career/open-positions/jobs_json_4.json
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
    
    
)




def scraper():
    '''
    ... scrape data from ALSO scraper.
    '''
    json_data = GetRequestJson("https://www.also.com/ec/cms5/en_6000/6000/company/career/open-positions/jobs_json_4.json")

    # read data from json_data and append it to job_list[]
    
    job_list = []
    for job in json_data['jobs']:
        if job['country'] == 'Romania': 
        # get jobs items from response
            job_list.append(Item(
                job_title = job['title'],
                job_link  = job['url'],
                company='ALSO',
                country= job['country'],
                county= 'București' if get_county('București')[-1] == True else get_county('București')[0],
                city='București',
                remote ="on-site" if "Internship" in job['title'] else "remote",
            ).to_dict())

    return job_list

def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ALSO"
    logo_link = 'https://upload.wikimedia.org/wikipedia/commons/f/fd/ALSO_Holding_AG_Logo_2020.svg'

    jobs = scraper()
    print("jobs found",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)
    
if __name__ == '__main__':
    main()
