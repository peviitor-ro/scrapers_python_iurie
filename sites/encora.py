#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Encora
# Link ------> https://boards-api.greenhouse.io/v1/boards/encora10/jobs
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
    ... scrape data from Encora scraper.
    '''
    json_data = GetRequestJson("https://boards-api.greenhouse.io/v1/boards/encora10/jobs")
    
    job_list = []
    location=["Craiova","Bucharest", "Romania"]
    for job in json_data['jobs']:
        for city in location:
            if  job["location"]["name"] ==  city :

                # get jobs items from response
                job_list.append(Item(
                    job_title=job["title"],
                    job_link=job["absolute_url"],
                    company="Encora",
                    country="România",
                    county="Bucuresti" if city=="Bucharest" else "all" if city=="Romania" else get_county_json(city),
                    city="Bucuresti" if city=="Bucharest" else "all" if city=="Romania" else city,
                    remote="hybrid",
                ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Encora"
    logo_link = "https://careers.encora.com/hubfs/Jobs_Microsite/encora-jobs-logo.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
