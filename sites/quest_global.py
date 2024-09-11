#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Quest global
# Link ------> https://careers.quest-global.com/widgets
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
import requests
import json



def scraper():
    '''
    ... scrape data from Quest global scraper.
    https://careers.quest-global.com/global/en/search-results?qcountry=Romania
    '''
    # post_data = PostRequestJson("https://careers.quest-global.com/widgets", custom_headers=headers, data_raw=data_raw)

    job_list = []
    url = "https://careers.quest-global.com/widgets"

    payload = json.dumps({
    "sortBy": "",
    "subsearch": "",
    "from": 0,
    "jobs": True,
    "counts": True,
    "all_fields": [
        "category",
        "type",
        "country",
        "state",
        "city",
        "Experience_Level",
        "phLocSlider"
    ],
    "pageName": "search-results",
    "size": 10,
    "clearAll": False,
    "jdsource": "facets",
    "isSliderEnable": True,
    "pageId": "page3",
    "siteType": "external",
    "keywords": "",
    "global": True,
    "selected_fields": {
        "country": [
        "Romania"
        ]
    },
    "locationData": {
        "sliderRadius": 305,
        "aboveMaxRadius": True,
        "LocationUnit": "miles"
    },
    "s": "1",
    "lang": "en_global",
    "deviceType": "desktop",
    "country": "global",
    "refNum": "QGRQGAGLOBAL",
    "ddoKey": "eagerLoadRefineSearch"
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'PHPPPE_ACT=8a7059ff-a448-4aab-9680-047a39777b6a; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiI4YTcwNTlmZi1hNDQ4LTRhYWItOTY4MC0wNDdhMzk3NzdiNmEifSwibmJmIjoxNzIxNjMwMDM1LCJpYXQiOjE3MjE2MzAwMzV9.ECK461YpO3bkwJPgI3_FhLffMaDKeh9NCGZIrByIPnM; VISITED_COUNTRY=global; VISITED_LANG=en'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.json()["eagerLoadRefineSearch"]["data"]["jobs"]
    
    for job in data:
        title=job["title"].replace(" ","-")
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"],
            job_link="https://careers.quest-global.com/global/en/job/"+job["jobId"]+"/"+title,
            company='Quest global',
            country="România",
            county="all" if not job["city"] else get_county_json(job["city"]),
            city="all" if not job["city"] else job["city"],
            remote="remote" if not job["city"] else "on-site",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Quest global"
    logo_link = "https://cdn.phenompeople.com/CareerConnectResources/QGRQGAGLOBAL/images/Header-1707137167631.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
