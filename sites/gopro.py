#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Gopro
# Link ------> https://jobs.gopro.com/api/v1/jobs/external
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
    ... scrape data from Gopro scraper.
        https://jobs.gopro.com/jobs/country/romania#/
    '''
    url = "https://jobs.gopro.com/api/appSearch"
    
    payload = {
        "query": "",
        "search_fields": {
            "title": {},
            "location": {},
            "category": {},
            "city_filter": {},
            "country_filter": {}
        },
        "result_fields": {
            "title": {
            "raw": {}
            },
            "location": {
            "raw": {}
            },
            "job_type": {
            "raw": {}
            },
            "content": {
            "snippet": {
                "fallback": True
            }
            },
            "category": {
            "raw": {}
            },
            "country_filter": {
            "raw": {}
            },
            "city_filter": {
            "raw": {}
            },
            "url": {
            "raw": {}
            }
        },
        "page": {
            "size": 40,
            "current": 1
        },
        "facets": {
            "category": {
            "type": "value",
            "size": 40
            },
            "location": {
            "type": "value",
            "size": 40
            },
            "job_type": {
            "type": "value",
            "size": 30
            }
        },
        "filters": {
            "all": [
            {
                "any": [
                {
                    "group_id": 2082
                }
                ]
            },
            {
                "any": [
                {
                    "live": 1
                }
                ]
            },
            {
                "country_filter": "romania"
            }
            ]
        }
        }
    headers = {
    'x-xsrf-token': 'eyJpdiI6Inp2VWVERTQ4SkxlV2VOY0dZL0Z5R2c9PSIsInZhbHVlIjoiTHNIN1lyK1QxUXhIQUEzV0xMYnA4SFVwU2tMYkdpYXU3U3VnTndUaER3ZTh3T0JQV1FxeTUrb1h4WTFJN09EcjRJWUNDMWV6Ui9SK3d3bSswRlJsZ1RKM2F6THNFT0lESmlDVUdKYVRwbUlYeWUyRW1rN1VlRnZMV3RvNk9hQjYiLCJtYWMiOiI5NDE2ODRjMDU5MTU3YzUzM2UzYTNlNTM4YWZjNzlmNWIwYWY4MGZmOWY1MDIyZTBhYjBlZDMxMjI5YmFmYWJkIiwidGFnIjoiIn0=',
    'Content-Type': 'application/json',
    'Cookie': 'XSRF-TOKEN=eyJpdiI6IlUyRmwxRG91OGhYdkxRelo5L2duZkE9PSIsInZhbHVlIjoiMDRWMjM4SXJaWGZiUnZidU1GY3VaQ0hZTmx1Y3VoamJwNGNhRTNZYldaQnZHaVZick1oeXBDQUsvQXlVVjRXL1ZuTDBlRFIrRGo4U0NEdmlwUlB3NThENzU2YmVjeTUxb2tVSk91NzVFMnlGTjE4NTdsd0FLQmZNMUdhYmJqR0kiLCJtYWMiOiIzNjczZWY5ZTg4Y2VlYzI5ZTNmOTRlNTE2YWFkM2RiODBiY2YxYTNiNWFlYjBlMmJiMjYyZTRmM2U5YmRlZDZmIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IlltWTkvMko5N2lVaFRpRWJwSFdHVmc9PSIsInZhbHVlIjoiTURkYVN3WXhMRS9JcVZoTllUeC95dWV0SG5vSXBZMkVOOFNranYvUjhlbTFnNUhhcnNQeUkra3VNbG9FOWhUdUF5SXNWL3Zlbm01UmQxZEh4S2pwTUs4MEU5WHlhZ0pIc2hYMjZPK3lDYkY2eGowV1g3RUYrTUNVeTR2TGV6dmQiLCJtYWMiOiI4NDhkNDg1ZmNlYjdkMTdiNjgwMThkYzg1OTg1ZDE2ODMxYTJhNjBiMjI2OGY1MjVlMTM1MDFlMmEyOTE3NjY0IiwidGFnIjoiIn0%3D'
    }

    post_data = PostRequestJson(url=url, custom_headers=headers, data_json=payload)

    job_list = []

    for job in post_data["results"]:
        city ="Bucuresti" if "bucharest" in job["city_filter"]["raw"] else job["city_filter"]["raw"]
        job_type = job["job_type"]["raw"].lower()
    

        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"]["raw"],
            job_link="https://jobs.gopro.com/en/us/jobs/"+job["url"]["raw"],
            company='Gopro',
            country="România",
            county="all" if "remote" in job_type else get_county_json(city),
            city="all" if "remote" in job_type else city,
            remote=job_type,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Gopro"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/c/c3/GoPro_logo.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
