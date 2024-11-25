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
    url = "https://ongig-ebdb.ent.us-west-2.aws.found.io/api/as/v1/engines/jobs-production/search.json"
    payload = {
        "query": "",
        "facets": {
            "category": {
                "type": "value",
                "size": 30
            },
            "location": {
                "type": "value",
                "size": 30
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
                            "location": "Remote Romania"
                        }
                    ]
                },
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
                }
            ]
        },
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

            "url": {
                "raw": {}
            }
        },
        "page": {
            "size": 5,
            "current": 1
        }
    }
    headers = {
        'authorization': 'Bearer search-8d5tkzjx1w7fi6sqkbqu4274',
        'Content-Type': 'application/json'
    }

    post_data = PostRequestJson(
        url=url, custom_headers=headers, data_json=payload)

    job_list = []

    for job in post_data["results"]:
        location = get_job_type(job["location"]["raw"])

        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"]["raw"],
            job_link="https://jobs.gopro.com/en/us/jobs/"+job["url"]["raw"],
            company='Gopro',
            country="România",
            county="all" if "remote" in location else location,
            city="all" if "remote" in location else location,
            remote=job["job_type"]["raw"],
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
