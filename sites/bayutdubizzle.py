#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> BayutDubizzle
# Link ------> https://apply.workable.com/api/v3/accounts/bayutdubizzle/jobs
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
    PostRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
import json


def scraper():
    '''
    ... scrape data from BayutDubizzle scraper.
    '''

    url = "https://apply.workable.com/api/v3/accounts/bayutdubizzle/jobs"

    payload = json.dumps({
        "query": "",
        "department": [],
        "location": [
            {
            "country": "Romania",
            "region": "",
            "city": "",
            "countryCode": "RO"
            }
        ],
        "remote": [],
        "workplace": [],
        "worktype": []
        })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': '__cf_bm=tO3SCRFZ993lwXSIdTCbsVcgWep3AUuZ0HbKCJ13r.o-1718010603-1.0.1.1-tZ3k9oMd0LDG4wpG4B1xyCbuGnMFqPN.8bfk197UR9ZgyKq5T1lg.eEPq1I_CSxsJm4U1EPPF6VB30Ka7W2p1w; wmc=%7B%22cookie_id%22%3A%22123655eb-9ffe-4e83-9c1a-fbf9d244dfe9%22%7D'
        }

    post_data = PostRequestJson(url=url, custom_headers=headers, data_raw=payload)
    job_list = []
    for job in post_data["results"]:
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"],
            job_link="https://apply.workable.com/bayutdubizzle/j/"+job["shortcode"],
            company='bayutdubizzle',
            country="România",
            county=job["location"]["region"].split()[0],
            city=job["location"]["city"],
            remote=job["workplace"].replace("_","-") if "_"in job["workplace"] else job["workplace"],
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "bayutdubizzle"
    logo_link = "https://media.licdn.com/dms/image/D4D16AQHo2EGgKPfjpw/profile-displaybackgroundimage-shrink_200_800/0/1665470872665?e=2147483647&v=beta&t=cSICEYbmur10j9QwcTfHuWi7LaVCwKbimBhv6tTS_UA"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
