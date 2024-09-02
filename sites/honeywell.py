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
from math import ceil
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
    "size": 50,
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
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': 'PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiJjYjNkYzFiYy02OWZkLTQ3M2QtOTFjMS00MzgzMmMyMzgyOGUifSwibmJmIjoxNzI1MDM1MTgxLCJpYXQiOjE3MjUwMzUxODF9.38bcQG081iCKUU4WomJxtTyY6Msvirk4YgXvPdpA-eE; PHPPPE_ACT=cb3dc1bc-69fd-473d-91c1-43832c23828e; VISITED_LANG=en; VISITED_COUNTRY=us; Per_UniqueID=191a41bf87a574-1aeaa0-add9-191a41bf87b7a1; OptanonAlertBoxClosed=2024-08-30T16:26:26.127Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Aug+30+2024+18%3A28%3A34+GMT%2B0200+(Central+European+Summer+Time)&version=202405.2.0&browserGpcFlag=1&isIABGlobal=false&hosts=&consentId=59c33013-54d6-4858-ac8f-5b8cd46c8d29&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A0%2CC0002%3A0%2CC0004%3A0&intType=2&geolocation=PL%3B12&AwaitingReconsent=false; PHPPPE_ACT=9943d118-2367-4dbe-a428-afce0f17c1f0; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiI5OTQzZDExOC0yMzY3LTRkYmUtYTQyOC1hZmNlMGYxN2MxZjAifSwibmJmIjoxNzI1MDM2MTAxLCJpYXQiOjE3MjUwMzYxMDF9.JkXrYwjFBYntrhCy0v6TGCnTKYnCi2OwH5Dnj3Gb5_4; VISITED_COUNTRY=us; VISITED_LANG=en',
    'origin': 'https://careers.honeywell.com',
    'priority': 'u=1, i',
    'referer': 'https://careers.honeywell.com/us/en/campaign-emea-ro-jobs?from=40&s=1&rk=l-campaign-emea-ro-jobs',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-csrf-token': 'dd64e703b2b44953a4093d9b6e0e088b'
    }
    
    post_data = PostRequestJson( "https://careers.honeywell.com/widgets", custom_headers=headers, data_json=payload)
    totalJobs=post_data["eagerLoadRefineSearch"]["totalHits"]
    pages=ceil(totalJobs/50)
    
    job_list = []
    for page in range(1, pages+1):
        
        for job in post_data["eagerLoadRefineSearch"]["data"]["jobs"]:
            # trebuie de facut restul job are 91
            # print(job["title"])
            # get jobs items from response
            job_list.append(Item(
                job_title=job["title"],
                job_link="https://careers.honeywell.com/us/en/job/" +job["jobId"]+"/",
                company='Honeywell',
                country="România",
                county=job["state"].title(),
                city="Bucuresti" if "Bucharest" == job["city"] else job["city"],
                remote=get_job_type(job["title"].lower()),
            ).to_dict())
            
        payload["from"]=page*50
        
        post_data = PostRequestJson( "https://careers.honeywell.com/widgets", custom_headers=headers, data_json=payload)
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
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
