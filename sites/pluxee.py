"""

Config for Dynamic Post Method -> For Json format!

Company ---> pluxee
Link ------> https://pluxee.wd3.myworkdayjobs.com/wday/cxs/pluxee/Pluxee_Career_Site/jobs

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

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
    ... scrape data from pluxee scraper.
    """
    url = "https://pluxee.wd3.myworkdayjobs.com/wday/cxs/pluxee/Pluxee_Career_Site/jobs"
    payload = {
        "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
        "limit": 20,
        "offset": 0,
        "searchText": "",
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Cookie": "PLAY_SESSION=4ceaadacdf48f7563d0d79255791ff192329b937-pluxee_pSessionId=1vk4coij12sdlrncgce0d2m5rj&instance=vps-prod-8d3cc5jy.prod-vps.pr502.cust.dub.wd; __cf_bm=1A5s2VTHcBnaFrgJCcG7dQY38pmMhFvf9d4VAnYEVLo-1740488095-1.0.1.1-diUkA1BtNeMVFeynvIyDrWcEwAaoH7VZnZ9XcGy0olrBBBVxcagICkYotDggH1fvR_p_p_xqhEH1f1GZuyPYmQ; __cflb=02DiuJFb1a2FCfph91mEfCE19uWmaV9PEYyoerFcEsnha; _cfuvid=JeKGcod7LE1ZnXtdkYhLX1163aE1O5ziCh3U650.wWs-1740488095964-0.0.1.1-604800000; wd-browser-id=0daaa235-406b-405f-8a90-6a61ba1828ab; wday_vps_cookie=1213831434.53810.0000",
    }
    post_data = PostRequestJson(url=url, custom_headers=headers, data_json=payload)
    base_url = "https://pluxee.wd3.myworkdayjobs.com/en-US/Pluxee_Career_Site"
    job_list = []
    for job in post_data["jobPostings"]:
        location = (
            "Bucuresti"
            if "Bucharest" == job["bulletFields"][1]
            else job["bulletFields"][1]
        )

        # get jobs items from response
        job_list.append(
            Item(
                job_title=job["title"],
                job_link=f"{base_url}{job["externalPath"]}",
                company="pluxee",
                country="România",
                county=get_county_json(location),
                city=location,
                remote="on-site",
            ).to_dict()
        )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "pluxee"
    logo_link = "https://ps-cdn1.imgix.net/uploads/1895/images/4c01305b85a0fbeea68d158743fcbad1da2c7ec7.png?auto=format%2Ccompress"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
