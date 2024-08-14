#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Vibracoustic
# Link ------> https://jobs.freudenberg.com/Freudenberg/api/json/?company=VC&location=L_00000250
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
    ... scrape data from Vibracoustic scraper.
    '''
    # https://jobs.freudenberg.com/Freudenberg/?company=VC&location=RO
    json_data = GetRequestJson("https://jobs.freudenberg.com/Freudenberg/api/json/?company=VC&location=L_00000250")

    job_list = []
    for job in json_data['jobs']:

        # get jobs items from response
        job_list.append(Item(
            job_title=job["jobtitle"],
            job_link=job["deepLink"],
            company="Vibracoustic",
            country="România",
            county="Dej",
            city="Dej",
            remote="Hybrid",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Vibracoustic"
    logo_link = "https://www2.solique.ch/templateimages/Freudenberg/img/logos/Vibracoustic.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
