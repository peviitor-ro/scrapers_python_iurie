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
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,ro-RO;q=0.8,ro;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'locale=en; _ga=GA1.1.963048768.1688498124; _ga_C9CY922645=GS1.1.1688498124.1.1.1688498147.38.0.0; OptanonAlertBoxClosed=2023-07-04T19:15:47.305Z; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+04+2023+22%3A15%3A47+GMT%2B0300+(Eastern+European+Summer+Time)&version=202211.2.0&isIABGlobal=false&hosts=&consentId=6bda047b-e19c-429e-a5e6-ae72f79d82e3&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1&AwaitingReconsent=false',
        'Origin': 'https://kenvue.taleo.net',
        'Referer': 'https://kenvue.taleo.net/careersection/2/jobsearch.ftl?_gl=1*1w74hxb*_ga*OTYzMDQ4NzY4LjE2ODg0OTgxMjQ.*_ga_C9CY922645*MTY4ODQ5ODEyNC4xLjEuMTY4ODQ5ODEzMy41Mi4wLjA.',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': "?0'",
        'sec-ch-ua-platform': '"Windows"',
        'tz': 'GMT+02:00',
        'tzname': 'Europe/Warsaw'
    }
    payload = json.dumps({
        "multilineEnabled": True,
        "sortingSelection": {
            "sortBySelectionParam": "3",
            "ascendingSortingOrder": "false"
        },
        "fieldData": {
            "fields": {
                "KEYWORD": "",
                "LOCATION": "1493840260991",
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
                    "selectedValues": []
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
                    "selectedValues": []
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

    post_data = PostRequestJson(
        url=url, custom_headers=headers, data_raw=payload)
   
    job_list = []
    base_url = "https://kenvue.taleo.net/careersection/2/jobdetail.ftl?job="
    end_url = "&tz=GMT%2B02%3A00&tzname=Europe%2FWarsaw"
    for job in post_data["requisitionList"]:
        location = job["column"][1].split('-')[3].replace('"]', '')
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job["column"][0],
            job_link=base_url+job["contestNo"]+end_url,
            company="Kenvue",
            country="România",
            county=get_county_json(location),
            city=location,
            remote="on-site",
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
