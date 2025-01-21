#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Kenvue
# Link ------> https://kenvue.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233
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
    scrape data from Kenvue scraper.
    https://kenvue.taleo.net/careersection/2/jobsearch.ftl?lang=en&keyword=#
    '''
    url = "https://kenvue.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233"

    payload = json.dumps({
    "multilineEnabled": True,
    "sortingSelection": {
        "sortBySelectionParam": "3",
        "ascendingSortingOrder": "false"
    },
    "fieldData": {
        "fields": {
        "KEYWORD": "",
        "LOCATION": "",
        "CATEGORY": ""
        },
        "valid": True
    },
    "filterSelectionParam": {
        "searchFilterSelections": [
        {
            "id": "POSTING_DATE",
            "selectedValues": []
        },
        {
            "id": "LOCATION",
            "selectedValues": [
            "1493840260991"
            ]
        },
        {
            "id": "JOB_FIELD",
            "selectedValues": []
        }
        ]
    },
    "advancedSearchFiltersSelectionParam": {
        "searchFilterSelections": [
        {
            "id": "ORGANIZATION",
            "selectedValues": []
        },
        {
            "id": "LOCATION",
            "selectedValues": [
            "1493840260991"
            ]
        },
        {
            "id": "JOB_FIELD",
            "selectedValues": []
        },
        {
            "id": "JOB_NUMBER",
            "selectedValues": []
        },
        {
            "id": "URGENT_JOB",
            "selectedValues": []
        },
        {
            "id": "STUDY_LEVEL",
            "selectedValues": []
        },
        {
            "id": "WILL_TRAVEL",
            "selectedValues": []
        }
        ]
    },
    "pageNo": 1
    })
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'tzname': 'Europe/Warsaw',
    'Content-Type': 'application/json',
    'Cookie': 'locale=en'
    }

    post_data = PostRequestJson(
        url=url, custom_headers=headers, data_raw=payload)
   
    job_list = []
    base_url = "https://kenvue.taleo.net/careersection/2/jobdetail.ftl?job="
    end_url = "&tz=GMT%2B02%3A00&tzname=Europe%2FWarsaw"
    
    for job in post_data["requisitionList"]:
        location = job["column"][1].split('-')[2].replace('"]', '')
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job["column"][0],
            job_link=base_url+job["contestNo"]+end_url,
            company="Kenvue",
            country="România",
            county=get_county_json(location),
            city=location,
            remote="hybrid",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Kenvue"
    logo_link = "https://kenvue.taleo.net/careersection/theme/18211901/1715719507000/en/theme/images/Kenvue_logo_black.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
