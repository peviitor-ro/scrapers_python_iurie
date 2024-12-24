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
# Company ---> partnerd
# Link ------> https://partnerd.teamtailor.com/jobs
#
#
from __utils import (
    GetStaticSoup,
    update_location_if_is_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from partnerd scraper.
    """
    soup = GetStaticSoup("https://partnerd.teamtailor.com/jobs")

    job_list = []
    for job in soup.find_all("li", class_="w-full"):

        # extract job type
        job_types = job.find("span", class_="inline-flex items-center gap-x-2")
        if job_types:
            job_type = get_job_type(job_types.text.strip())
        else:
            job_type = "on-site"

        # Find location
        location_span = job.find("div", class_="mt-1 text-md").find_all('span')
        if len(location_span) == 1 or len(location_span) == 3:
            location = location_span[0].text

        elif len(location_span) == 5:
            location = location_span[2].text

        if location == "Online Dealer":
            location = "Bucharest"
        if location == "Bucharest":
            location = "Bucuresti"
        county = get_county_json(location)
        
        # print(update_location_if_is_county(counties=county, locations=location))
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("a").find("span").text,
            job_link=job.find("a").get("href"),
            company="partnerd",
            country="România",
            county=county,
            city=location,
            remote=job_type,
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "partnerd"
    logo_link = "https://uploads-ssl.webflow.com/61070548cd02cbe9343b5101/61070d5df465e95e28ce7183_Partnerd%20PNG%20Logo-p-500.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
