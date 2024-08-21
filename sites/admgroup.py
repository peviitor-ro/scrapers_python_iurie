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
    logo_link = "https://pinpoint-production.s3.eu-west-2.amazonaws.com/variants/0d4y4bslls5mj2e5s4nkazka32ky/3985fcd1f77d36d9f3e2d01f056248d4eb5d94046fae76707810629ddb0379fd?response-content-disposition=inline%3B%20filename%3D%22adm_logo.png%22%3B%20filename%2A%3DUTF-8%27%27adm_logo.png&response-content-type=image%2Fpng&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJ5PLDFLGL6OULNZQ%2F20240813%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240813T125322Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=eb224f24f232bc28e7e39d258ce23b95b6ba79bed6b992e06d8ca0d3ebe41e7a"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
