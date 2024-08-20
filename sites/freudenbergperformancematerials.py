#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> FREUDENBERGPERFORMANCEMATERIALS
# Link ------> https://jobs.freudenberg.com/Freudenberg/api/json/?company=FPM
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
    ... scrape data from FREUDENBERG  PERFORMANCE MATERIALS scraper.
    '''
    # https://jobs.freudenberg.com/Freudenberg/?company=FPM&location=RO
    json_data = GetRequestJson("https://jobs.freudenberg.com/Freudenberg/api/json/?company=FPM&location=L_00000038")

    job_list = []
    for job in json_data["jobs"]:
        # get jobs items from response
        job_list.append(Item(
            job_title=job["jobtitle"],
            job_link=job["deepLink"],
            company="FREUDENBERGPERFORMANCEMATERIALS",
            country="România",
            county="Braşov",
            city="Braşov",
            remote="remote" if "R" in job["externalId"] else "on-site",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "FREUDENBERGPERFORMANCEMATERIALS"
    logo_link = "https://www.freudenberg-pm.com/-/media/Images/Logos/FREUDENBERG_PERFORMANCE_MATERIALS.svg?h=48&w=294&la=en&hash=ACFC54066D4BB1FDBDAA4826B6F4A294"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
