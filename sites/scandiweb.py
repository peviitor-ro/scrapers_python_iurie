#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Scandiweb
# Link ------> https://scandiweb.pinpointhq.com/postings.json?location_id%5B%5D=33918&_=1720615242842
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
    ... scrape data from Scandiweb scraper.
    '''
    json_data = GetRequestJson("https://scandiweb.pinpointhq.com/postings.json?location_id%5B%5D=33918&_=1720615242842")

    job_list = []
    for job in json_data['data']:
        location = "București"  if job["location"]["city"]=="Bucharest" else job["location"]["city"]
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"],
            job_link=job["url"],
            company="Scandiweb",
            country="România",
            county=get_county_json(location),
            city=location,
            remote=job["workplace_type"],
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Scandiweb"
    logo_link = "https://app.pinpointhq.com/rails/active_storage/representations/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBeUxRYWc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--724bfe7b16b71eb428b60394fea2896a1c0e84ba/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaDdCam9MY21WemFYcGxTU0lRTkRRd0xqQjRNVEF3TGpBR09nWkZWQT09IiwiZXhwIjpudWxsLCJwdXIiOiJ2YXJpYXRpb24ifX0=--5fd990b5737f041b8b006e0f6f8b9bd3043c9631/ezgif.com-gif-maker%20(1).png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
