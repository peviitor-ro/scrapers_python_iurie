#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Beshapingthefuture
# Link ------> https://www.careers-page.com/api/v1.0/c/be-shaping-the-future/jobs/?page_size=50
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
    ... scrape data from Be Shaping the future scraper.
    '''
    headers = {
                'accept': 'application/json, text/plain, */*',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
                }
    json_data = GetRequestJson("https://www.careers-page.com/api/v1.0/c/be-shaping-the-future/jobs/?page_size=50", custom_headers=headers)

    job_list = []
    for job in json_data['results']:
        if job["country"]=="Romania":

        # get jobs items from response
            job_list.append(Item(
                job_title=job["position_name"],
                job_link="https://www.careers-page.com/be-shaping-the-future/job/"+job["hash"],
                company="Beshapingthefuture",
                country="România",
                county="Bucuresti" if job["city"]=="Bucharest" else get_county_json(job["city"]),
                city="Bucuresti" if job["city"]=="Bucharest" else job["city"] ,
                remote="on-site",
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Beshapingthefuture"
    logo_link = "https://manatal-backend-public-assets.s3.amazonaws.com/media/career_portal_logo_direct_upload/8338a5ba-a93a-411c-af26-dbffadfb8ebb_Be_STF_side.jpg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
