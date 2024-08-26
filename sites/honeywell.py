#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Honeywell
# Link ------> https://careers.honeywell.com/widgets
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


def scraper():
    '''
    ... scrape data from Honeywell scraper.
    '''
    payload = {
        "lang": "en_us",
        "deviceType": "desktop",
        "country": "us",
        "pageName": "Campaign EMEA RO Jobs",
        "ddoKey": "eagerLoadRefineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": 0,
        "jobs": True,
        "counts": True,
        "all_fields": [
            "country",
            "state",
            "city",
            "category",
            "WorkType",
            "experienceLevel",
            "phLocSlider"
        ],
        "pageType": "landingPage",
        "size": 95,
        "rk": "l-campaign-emea-ro-jobs",
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": True,
        "pageId": "page743-prod",
        "siteType": "external",
        "keywords": "",
        "global": True,
        "selected_fields": {
            "country": [
            "Romania"
            ]
        },
        "locationData": {
            "sliderRadius": 150,
            "aboveMaxRadius": True,
            "LocationUnit": "miles"
        },
        "rkstatus": True,
        "s": "1"
        }
    
    headers = {
    'Content-Type': 'application/json',
    }

    post_data = PostRequestJson("https://careers.honeywell.com/widgets", custom_headers=headers, data_json=payload)

    job_list = []
    for job in post_data["eagerLoadRefineSearch"]["data"]["jobs"]:
    
        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"],
            job_link="https://careers.honeywell.com/us/en/job/"+job["jobId"]+"/",
            company='Honeywell',
            country="România",
            county=job["state"],
            city="Bucuresti" if "Bucharest" == job["city"] else job["city"],
            remote=get_job_type(job["title"].lower()),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Honeywell"
    logo_link = "https://www.honeywell.com/content/dam/honeywellbt/en/images/logos/HON%20logo_200x37%202.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
