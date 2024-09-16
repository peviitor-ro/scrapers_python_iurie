#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Bosch
# Link ------> https://bosch-i3-caas-api.e-spirit.cloud/bosch-i3-prod/bosch-de.jobs.content/_aggrs/get_jobs?page=1&pagesize=100&avars=%7B%22country%22%3A%5B%22ro%22%5D%2C%22sort%22%3A%7B%22releasedDate%22%3A-1%7D%2C%22max_distance%22%3A30000%7D
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
    ... scrape data from Bosch scraper.
    https://jobs.bosch.com/en/?pages=1&maxDistance=30&distanceUnit=km&country=ro#
    '''
    headers = {
        'authorization': 'Bearer 19c815d0-6b97-4c7d-a966-e8cadb1f50ed'
    }
    job_list = []
    url = "https://bosch-i3-caas-api.e-spirit.cloud/bosch-i3-prod/bosch-de.jobs.content/_aggrs/get_jobs?page=1&pagesize=100&avars=%7B%22country%22%3A%5B%22ro%22%5D%2C%22sort%22%3A%7B%22releasedDate%22%3A-1%7D%2C%22max_distance%22%3A30000%7D"
    json_data = GetRequestJson(url=url, custom_headers=headers)
    page = 1

    while len(json_data["_embedded"]["rh:result"][0]["data"]) > 0:
        results = json_data["_embedded"]["rh:result"][0]["data"]
        for job in results:

            location = job["location"]["city"].split(",")[-1].strip()
        # get jobs items from response
            job_list.append(Item(
                job_title=job["name"],
                job_link="https://jobs.bosch.com/en/job/"+job["jobUrl"],
                company="Bosch",
                country="România",
                county=get_county_json(location),
                city=location,
                remote="remote" if job["location"]["remote"] else "hybrid",
            ).to_dict())
        # replace page to request new data from api
        url = url.replace(f"page={page}", f"page={page+1}")
        page += 1
        # make request with updated url
        json_data = GetRequestJson(url=url, custom_headers=headers)
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Bosch"
    logo_link = "https://www.pngmart.com/files/22/Bosch-Logo-PNG-HD.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
