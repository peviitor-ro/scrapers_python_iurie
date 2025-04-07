"""

Config for Dynamic Get Method -> For Json format!

Company ---> suvoda
Link ------> https://job-boards.greenhouse.io/embed/job_board?for=suvoda&offices%5B%5D=4000485002&offices%5B%5D=4059182002&_data=routes%2Fembed.job_board

"""

from __utils import (
    GetRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from suvoda scraper.
    """
    headers = {
        "accept": "*/*",
        "priority": "u=1, i",
        "referer": "https://job-boards.greenhouse.io/embed/job_board?for=suvoda&offices%5B%5D=4000485002",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }
    url = "https://job-boards.greenhouse.io/embed/job_board?for=suvoda&offices%5B%5D=4000485002&offices%5B%5D=4059182002&_data=routes%2Fembed.job_board"
    json_data = GetRequestJson(url=url, custom_headers=headers)

    job_list = []

    for job in json_data["jobPosts"]["data"]:

        # extract job location
        if "Romania" in job["location"]:
            if ";" in job["location"]:
                parts = job["location"].split(";")
                cities = []
                for part in parts:
                    # Extract city name by splitting at the comma and taking the first part
                    city = part.split(",")[0].strip()
                    cities.append(city)
            else:
                cities = job["location"].split(",")[0]

            # find county for city
            if isinstance(cities, list):
                counties = []
                for city in cities:
                    counties.append(get_county_json(city))
            else:
                counties = get_county_json(cities)

            # get jobs items from response
            job_list.append(
                Item(
                    job_title=job["title"],
                    job_link=job["absolute_url"],
                    company="Suvoda",
                    country="România",
                    county=counties,
                    city=cities,
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

    company_name = "suvoda"
    logo_link = "https://www.suvoda.com/hubfs/raw_assets/public/Suvoda2022/images/suvoda-logo-purple-fpo.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
