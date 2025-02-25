"""

 Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> Alight
Link ------> https://careers.alight.com/us/en/search-results?m=3&location=Virtual%2C%20Romania

"""

from __utils import (
    PostRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Alight scraper using selenium.
    """
    job_list = []

    url = "https://careers.alight.com/widgets"

    headers = {
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-csrf-token": "4ecd7fa9a9744338b707790ad81a8596",
        "Cookie": "PHPPPE_ACT=350d2a7b-a8dc-493e-8d3b-27072625842e; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiIzNTBkMmE3Yi1hOGRjLTQ5M2UtOGQzYi0yNzA3MjYyNTg0MmUifSwibmJmIjoxNzQwNDg1MTU0LCJpYXQiOjE3NDA0ODUxNTR9.GPzW530BnfgV3EYwVIc0_9lLtDinmkSy83vvJn_nJhc; VISITED_COUNTRY=us; VISITED_LANG=en",
    }
    payload = {
        "country": "",
        "pageName": "search-results",
        "ddoKey": "refineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": 0,
        "jobs": True,
        "counts": True,
        "all_fields": ["category", "country", "state", "city"],
        "size": 100,
        "clearAll": True,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page1",
        "siteType": "external",
        "location": "",
        "keywords": "",
        "global": True,
        "selected_fields": {},
        "locationData": {},
    }

    jobs = PostRequestJson(url=url, custom_headers=headers, data_json=payload)

    for job in jobs["refineSearch"]["data"]["jobs"]:
        if job["country"] == "Romania":
            location = "all" if "Virtual" == job["city"] else job["city"]
            county = get_county_json(location)
            # get jobs items from response
            job_list.append(
                Item(
                    job_title=job["title"],
                    job_link=f"https://careers.alight.com/us/en/job/{job["jobId"]}",
                    company="Alight",
                    country="România",
                    county=county,
                    city=location,
                    remote="remote" if location == "all" else "on-site",
                ).to_dict()
            )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Alight"
    logo_link = "https://cdn.phenompeople.com/CareerConnectResources/ALIGUS/en_us/mobile/assets/images/logo.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
