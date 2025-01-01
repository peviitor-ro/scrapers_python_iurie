#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> jolera
# Link ------> https://jolera.freshteam.com/hire/widgets/jobs.json
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
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from jolera scraper.
    https://www.jolera.com/careers/
    '''
    json_data = GetRequestJson(
        "https://jolera.freshteam.com/hire/widgets/jobs.json")

    job_list = []

    for job in json_data['jobs']:

        if job["branch_id"] == 4000038337:  # "id": 4000038337, for Bucharest, Romania"
            

            # get jobs items from response
            job_list.append(Item(
                job_title=job["title"],
                job_link=job["url"],
                company="Jolera",
                country="România",
                county="Bucuresti",
                city="Bucuresti",
                remote="on-site",
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "jolera"
    logo_link = "https://media.licdn.com/dms/image/v2/D4D0BAQGH2wI6rzmShw/company-logo_200_200/company-logo_200_200/0/1724181976196/jolera_logo?e=1743638400&v=beta&t=8os_nia7vLFMofklB0YW0AEJO6878_dyZoA514crQLE"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
