#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> AD/01
# Link ------> https://www.ad01.com/api/vacancy/?sort=created&sortDir=DESC
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
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from AD scraper.
    '''
    job_list = []
    links=["https://www.ad01.com/api/vacancy/?sort=created&sortDir=DESC",
           "https://www.ad01.com/api/vacancy/?pageNumber=2&sort=created&sortDir=DESC"]
    for link in links:
        json_data = GetRequestJson(link)
    
        for job in json_data['vacancies']:
            location="București" if "Bucharest" in job["city"] else job["city"]
            link="https://www.ad01.com/vacature/"+str(job['id'])+"/"+job['slug']

            # get jobs items from response
            job_list.append(Item(
                job_title=job["title"],
                job_link=link,
                company="Ad01",
                country="România",
                county=get_county_json(location),
                city=location,
                remote="hybrid",
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Ad01"
    logo_link = "https://www.ad01.com/uploads/logo%20(1).svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
