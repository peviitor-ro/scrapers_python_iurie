#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Tec:agenc
# Link ------> https://tecss.bamboohr.com/careers/list

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
    ... scrape data from Tec:agenc scraper.
    '''
    json_data = GetRequestJson("https://tecss.bamboohr.com/careers/list")

    job_list = []
    for job in json_data['result']:
        location  =  job['location']['city']
        check_county=get_county(location)[0]if True in get_county(location) else  None
      
        # get jobs items from response
        job_list.append(Item(
            job_title=job['jobOpeningName'],
            job_link="https://tecss.bamboohr.com/careers/"+job['id'],
            company="tec:agency",
            country="România",
            county=check_county if check_county else "Cluj",
            city=location,
            remote="hybrid" if job['locationType'] == '2' else "on-site",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "tec:agency"
    logo_link = "https://images.crunchbase.com/image/upload/c_pad,h_256,w_256,f_auto,q_auto:eco,dpr_1/vnutwbrcrrafaausnjxd"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
