#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> RolandBerger
# Link ------> https://rolandberger-search-api.e-spirit.cloud/v1/prepared_search/JoinJobs/execute/?language=en&query=*
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
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """_summary_
    scrape data from RolandBerger scraper.
    Returns:
        Job_dict 
    """

    json_data = GetRequestJson("https://rolandberger-search-api.e-spirit.cloud/v1/prepared_search/JoinJobs/execute/?language=en&query=*")

    job_list = []
    for job in json_data['results']:
        if job["location"]==["Bucharest"]:
            # get jobs items from response
            job_list.append(Item(
                job_title=job["title"][0],
                job_link=job["positionProfile___webAddress"][0],
                company="Rolandberger",
                country="România",
                county="București",
                city="București",
                remote="on-site",
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Rolandberger"
    logo_link = "https://pr-journal.de/images/stories/logos/Roland_Berger_Logo.jpg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
