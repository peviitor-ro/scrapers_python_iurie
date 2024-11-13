#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> wipro
# Link ------> https://careers.wipro.com/api/jobs?location=Romania
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
    ... scrape data from wipro scraper.
    https://careers.wipro.com/careers-home/jobs?location=Romania&woe=12&stretchUnit=KILOMETERS&stretch=25&page=1&limit=100
    '''
    payload = {}
    headers = {
        'Cookie': 'jasession=s%3AbvTw0yJbnTUE_qNcLKc1fz1hJkYuqBNC.uOayx7V2I3cUqUjNsdMPtvoJ%2B1Cmy1HWF%2BukgiMTWKc; searchSource=external'
    }
    json_data = GetRequestJson(
        "https://careers.wipro.com/api/jobs?location=Romania&page=1&limit=100", custom_headers=headers)

    job_list = []
    for job in json_data['jobs']:
        city = job["data"]["city"].capitalize().replace("-wsm1", "")
        city = "Bucuresti" if "Bucharest" in city else city

        # get jobs items from response
        job_list.append(Item(
            job_title=job["data"]["title"],
            job_link=job["data"]["meta_data"]["canonical_url"],
            company="wipro",
            country="România",
            county=get_county_json(city),
            city=city,
            remote=get_job_type(job["data"]["description"]),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "wipro"
    logo_link = "https://cms.jibecdn.com/prod/wipro/assets/HEADER-NAV_LOGO-en-us-1698423772812.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
