#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> EsteeLauderCompanies
# Link ------> https://jobs.elcompanies.com/api/jobs?page=1&location=Romania&keywords=&stretchUnit=KILOMETERS&limit=100&woe=12&stretch=10&sortBy=relevance&descending=false&internal=false&deviceId=undefined&domain=esteelauder.jibeapply.com
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
    ... scrape data from EsteeLauderCompanies scraper.
    https://jobs.elcompanies.com/estee-lauder-companies/jobs?page=1&location=Romania&keywords=&stretchUnit=KILOMETERS&limit=100&woe=12&stretch=10
    '''
    json_data = GetRequestJson(
        "https://jobs.elcompanies.com/api/jobs?page=1&location=Romania&keywords=&stretchUnit=KILOMETERS&limit=100&woe=12&stretch=10&sortBy=relevance&descending=false&internal=false&deviceId=undefined&domain=esteelauder.jibeapply.com")

    job_list = []
    for job in json_data['jobs']:

        # get jobs items from response
        job_list.append(Item(
            job_title=job["data"]["title"],
            job_link=job["data"]["meta_data"]["canonical_url"],
            company="Estee Lauder Companies",
            country="România",
            county="București" if "Bucuresti" in job["data"]["state"] else job["data"]["state"],
            city="București" if "Bucharest" in job["data"]["city"] else job["data"]["city"],
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Estee Lauder Companies"
    logo_link = "https://www.moodiedavittreport.com/wp-content/uploads/2020/01/Screenshot-2019-11-18-at-20.50.11-1.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
