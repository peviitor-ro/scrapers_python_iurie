#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> ABB
# Link ------> https://careers.abb/widgets
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
    GetDataCurl,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from ABB scraper.
        https://careers.abb/global/en/search-results
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-csrf-token': '1b3cc21abbd141b7a86bd202f48b964d',
        'Content-Type': 'application/json',
        'Cookie': 'PHPPPE_ACT=f128b2bf-862e-4a64-a729-bded71146bda; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiJmMTI4YjJiZi04NjJlLTRhNjQtYTcyOS1iZGVkNzExNDZiZGEifSwibmJmIjoxNzI2NDgwNzMzLCJpYXQiOjE3MjY0ODA3MzN9.xHVJwjDMrjOibt6WlIzZg5ZbpJMmhsCGt9H3BVI4FFA'
    }
    payload = {
        "country": "global",
        "pageName": "search-results",
        "ddoKey": "refineSearch",
        "subsearch": "",
        "from": 0,
        "jobs": True,
        "all_fields": [
            "category",
            "subCategory",
            "businessSegment",
            "businessSegmentDescr",
            "continent",
            "country",
            "city",
            "contractType",
            "jobLevel",
            "jobType"
        ],
        "size": 99,
        "clearAll": False,
        "jdsource": "facets",
        "selected_fields": {
            "country": [
                    "Romania"
            ]
        },
        "locationData": {}
    }
    post_data = PostRequestJson(
        "https://careers.abb/widgets", custom_headers=headers, data_json=payload)

    job_list = []
    for job in post_data["refineSearch"]["data"]["jobs"]:
        title = job["title"]
        link = "https://careers.abb/global/en/job/" + \
            job["reqId"]+"/"+title.replace(' ', '-').replace('---', '-')
    
        # get jobs items from response
        job_list.append(Item(
            job_title=title,
            job_link=link,
            company='ABB',
            country="România",
            county="Bucuresti",
            city="Bucuresti",
            remote=get_job_type(job["descriptionTeaser"]),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ABB"
    logo_link = "https://cdn.phenompeople.com/CareerConnectResources/ABB1GLOBAL/en_global/desktop/assets/images/v-1711026688514-header-logo.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
