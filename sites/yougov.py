#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> yougov
# Link ------> https://jobs.yougov.com/jobs
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
    GetCustumRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
import json


def scraper():
    '''
    ... scrape data from yougov scraper.

    '''
    url = "https://jobs.yougov.com/api/jobs?"

    payload = {}
    headers = {
        'Cookie': 'incap_ses_687_1896749=2Z60ZWAc1Q0XyQF3CLeICfzXPWcAAAAACBM67qQJ/0s0CW/yxNIafw==; visid_incap_1896749=/Krsl4hZQfySjidEP/Y9k2/PPWcAAAAAQUIPAAAAAABlw+mipio9ulDebLIFwwhR'
    }

    data = GetCustumRequestJson(url=url, headers=headers, payload=payload)
    job_list = []

    for job in data:
        if job["country"] == "Romania":

            # get jobs items from response
            job_list.append(Item(
                job_title=job["title"],
                job_link=job["url"],
                company="Yougov",
                country="România",
                county="Bucuresti" if "Bucharest" in job["city"] else get_county_json(
                    job["city"]),
                city="Bucuresti" if "Bucharest" in job["city"] else job["city"],
                remote="on-site",
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "yougov"
    logo_link = "https://jobs.yougov.com/assets/images/logos-patterns/logo-dark.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
