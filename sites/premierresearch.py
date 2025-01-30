"""

 Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> premierresearch
Link ------> https://premier-research.com/our-company/careers/?locations=Romania

"""
from __utils import (
    PostRequestJson,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
def scraper():
    '''
         scrape data from premierresearce scraper.
         https://premierresearch.wd12.myworkdayjobs.com/PremierResearch?locations=9e662c32237d10020998e40b53a80000
    '''
    job_list = []
    base_link = "https://premierresearch.wd12.myworkdayjobs.com/en-US/PremierResearch"

    url = "https://premierresearch.wd12.myworkdayjobs.com/wday/cxs/premierresearch/PremierResearch/jobs"

    payload = {
        "appliedFacets": {
            "locations": ["9e662c32237d10020998e40b53a80000"]
        },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    post_data = PostRequestJson(url=url,  data_json=payload)

    for job in post_data["jobPostings"]:
   
        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"],
            job_link=base_link+job["externalPath"] +
            "?locations=9e662c32237d10020998e40b53a80000",
            company="Premierresearch",
            country="România",
            county="Bucuresti",
            city="Bucuresti",
            remote="remote",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "premierresearch"
    logo_link = "https://premier-research.com/wp-content/uploads/2019/04/Premier-Logo.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
