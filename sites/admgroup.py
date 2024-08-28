#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> admgroup
# Link ------> https://admgroup.pinpointhq.com/postings.json?location_id%5B%5D=31893
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
    ... scrape data from adm group scraper.
    '''
    # https://admgroup.pinpointhq.com/?location_id=%5B31893%5D
    json_data = GetRequestJson("https://admgroup.pinpointhq.com/postings.json?location_id%5B%5D=31893")

    job_list = []
    for job in json_data['data']:

        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"],
            job_link=job["url"],
            company="admgroup",
            country="România",
            county="Bucuresti" if"Bucharest" == job["location"]["city"] else get_county_json(job["location"]["city"]),
            city="Bucuresti" if"Bucharest" == job["location"]["city"] else job["location"]["city"],
            remote=job["workplace_type_text"],
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "admgroup"
    logo_link = "https://www.admgroup.com/media/4n3jiiev/adm_logo.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
