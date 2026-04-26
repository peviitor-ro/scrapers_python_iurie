#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> AD/01
# Link ------> https://www.ad01.com/api/vacancy/?sort=created&sortDir=DESC
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
    get_county_json,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from AD scraper.
    '''
    job_list = []
    headers = {"X-Requested-With": "XMLHttpRequest"}
    base_url = "https://www.ad01.com/api/vacancy/?sort=created&sortDir=DESC"
    json_data = GetRequestJson(base_url, custom_headers=headers)

    total_pages = json_data.get("meta", {}).get("totalPageCount", 1)

    for page_number in range(1, total_pages + 1):
        link = f"{base_url}&pageNumber={page_number}"
        json_data = GetRequestJson(link, custom_headers=headers)

        for job in json_data["vacancies"]:
            location="București" if "Bucharest" in job["city"] else job["city"]
            link="https://www.ad01.com/vacature/"+str(job['id'])+"/"+job['slug']

            # get jobs items from response
            job_list.append(Item(
                job_title=job["title"],
                job_link=link,
                company="Ad01",
                country="România",
                county=get_county_json(location),
                city=location,
                remote="hybrid",
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Ad01"
    logo_link = "https://www.ad01.com/uploads/logo%20(1).svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
