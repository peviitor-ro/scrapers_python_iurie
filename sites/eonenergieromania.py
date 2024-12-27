#
#
#  Basic for scraping data from static pages
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> Delgaz
# Link ------> https://careers.eon.com/romania/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=&optionsFacetsDD_city=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield3=
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
    """
    ... scrape data from EON Energie România scraper.
    https://jobs.eon.com/en?locale=en_GB&filter=locations.country%3ARomania%2Ccompany%3AE.ON+Energie+Romania
    """

    job_list = []
    url = "https://v09fm4cjghdr23p7p.a1.typesense.net/multi_search?x-typesense-api-key=AGw1v6TzYYkkQyvvf6uFvHXuO3DML7AD"

    payload = "{\"searches\":[{\"collection\":\"eon_en\",\"q\":\"*\",\"query_by\":\"data.title,data.idClient,data.jobNumber,data.company,data.recruiter,data.locations.city,content.task,content.profile,content.offer,content.contact\",\"infix\":\"always,always,always,always,off,off,off,off,off,off\",\"drop_tokens_threshold\":0,\"num_typos\":\"1,0,0,1,0,0,0,0,0,0\",\"filter_by\":\"((data.company:=[`E.ON Energie Romania`] && data.locations.country:=[`Romania`]) && data.company:!=Westconnect GmbH)\",\"sort_by\":\"_text_match:desc,data.postingDate_timestamp:desc\",\"page\":1,\"per_page\":40,\"facet_by\":\"data.businessUnit,data.category,data.company,data.contract,data.employmentType,data.classification,data.entryLevel,data.jobField,data.language,data.remote,data.locations.city,data.locations.cityState,data.locations.state,data.locations.country\",\"max_facet_values\":500,\"include_fields\":\"data,_geoloc\",\"split_join_tokens\":\"always\",\"typo_tokens_threshold\":2},{\"collection\":\"eon_en\",\"q\":\"*\",\"query_by\":\"data.title,data.idClient,data.jobNumber,data.company,data.recruiter,data.locations.city,content.task,content.profile,content.offer,content.contact\",\"infix\":\"always,always,always,always,off,off,off,off,off,off\",\"drop_tokens_threshold\":0,\"num_typos\":\"1,0,0,1,0,0,0,0,0,0\",\"filter_by\":\"data.company:=[`E.ON Energie Romania`]\",\"sort_by\":\"_text_match:desc,data.postingDate_timestamp:desc\",\"page\":1,\"per_page\":0,\"facet_by\":\"data.locations.cityState,data.locations.state,data.locations.country\",\"max_facet_values\":500,\"include_fields\":\"\",\"split_join_tokens\":\"always\",\"typo_tokens_threshold\":2},{\"collection\":\"eon_en\",\"q\":\"*\",\"query_by\":\"data.title,data.idClient,data.jobNumber,data.company,data.recruiter,data.locations.city,content.task,content.profile,content.offer,content.contact\",\"infix\":\"always,always,always,always,off,off,off,off,off,off\",\"drop_tokens_threshold\":0,\"num_typos\":\"1,0,0,1,0,0,0,0,0,0\",\"filter_by\":\"data.locations.country:=[`Romania`]\",\"sort_by\":\"_text_match:desc,data.postingDate_timestamp:desc\",\"page\":1,\"per_page\":0,\"facet_by\":\"data.company\",\"max_facet_values\":500,\"include_fields\":\"\",\"split_join_tokens\":\"always\",\"typo_tokens_threshold\":2}]}"
    headers = {
        'Content-Type': 'text/plain'
    }

    post_data = PostRequestJson(
        url=url, custom_headers=headers, data_raw=payload)

    for job in post_data["results"][0]["hits"]:
        if len(job["document"]["data"]["locations"]) > 1:

            cities = [location['city']
                      for location in job["document"]["data"]["locations"]]
            counties = [county["state"]
                        for county in job["document"]["data"]["locations"]]
        else:
            cities = job["document"]["data"]["locations"][0]["city"]
            counties = job["document"]["data"]["locations"][0]["state"]

        # get jobs items from response
        job_list.append(Item(
            job_title=job["document"]["data"]["title"],
            job_link=job["document"]["data"]["jobBoard_link"],
            company="E.ON Energie România",
            country="România",
            county=counties,
            city=cities,
            remote=job["document"]["data"]["remote"].lower(),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "E.ON Energie România"
    logo_link = "https://www.eon-romania.ro/content/dam/eon/eon-romania-ro/logo/header_M.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
