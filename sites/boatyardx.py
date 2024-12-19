#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> boatyardx
# Link ------> https://boatyardx.hirehive.com/api/v1/jobs
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
    ... scrape data from boatyardx scraper.
    '''
    json_data = GetRequestJson("https://boatyardx.hirehive.com/api/v1/jobs")

    job_list = []
    for job in json_data['jobs']:
        location=job["location"].strip().split(" / ")
        cities=['Cluj-Napoca', 'Iasi']  if "Remote" in location else location
        county=["Iasi" if city=="Iasi" else get_county_json(city) for city in cities]
        print(cities)
        print(county)
        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"],
            job_link=job["hostedUrl"],
            company="Boatyardx",
            country="România",
            county=county,
            city=cities,
            remote="remote" if "Remote" in location else get_job_type(job["description"]["text"]),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "boatyardx"
    logo_link = "https://image.pitchbook.com/QvjznJQKgJJQcS1ByZ2uMXAWp3d1668772609434_200x200"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    # UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
