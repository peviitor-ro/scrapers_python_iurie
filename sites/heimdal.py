"""

Config for Dynamic Get Method -> For Json format!

Company ---> heimdal
Link ------> https://heimdalsecurity.bamboohr.com/careers/list
            https://heimdalsecurity.bamboohr.com/careers

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

"""

from __utils import (
    GetRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
import json


def scraper():
    """
    ... scrape data from heimdal scraper.
    """
    json_data = GetRequestJson("https://heimdalsecurity.bamboohr.com/careers/list")
    base_url = "https://heimdalsecurity.bamboohr.com/careers/"
    job_types = {"0": "on-site", "1": "remote", "2": "hybrid"}

    job_list = []
    for job in json_data["result"]:
        if job["atsLocation"]["country"] == "Romania":
            city = (
                "all"
                if "all" in job["atsLocation"]["city"].lower()
                else job["location"]["city"]
            )
            state = (
                "all" if job["location"]["state"] == None else job["location"]["state"]
            )
            job_type = ""
            # extract job type from dict
            for key, value in job_types.items():
                if job["locationType"] == key:
                    job_type = value

            # get jobs items from response
            job_list.append(
                Item(
                    job_title=job["jobOpeningName"],
                    job_link=f"{base_url}{job["id"]}",
                    company="Heimdal",
                    country="România",
                    county=state,
                    city=city,
                    remote=job_type,
                ).to_dict()
            )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "heimdal"
    logo_link = "https://heimdalsecurity.com/wp-content/themes/heimdal/img/book-a-demo/heimdal-logo.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
