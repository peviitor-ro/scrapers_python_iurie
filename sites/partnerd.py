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
    job_list = []
    url = "https://partnerd.teamtailor.com/jobs?page=1&query=&split_view=true"


    while True:
        soup = GetStaticSoup(url)

        for job in soup.find_all("li", class_="w-full"):

            # extract job type
            job_types = job.find("span", class_="inline-flex items-center gap-x-2")
            if job_types:
                job_type = get_job_type(job_types.text.strip())
            else:
                job_type = "on-site"

            # Find location
            location_div = job.find("div", class_="mt-4 text-md")
            if not location_div:
                continue
            location_span = location_div.find_all('span')
            location = location_span[-1].text.strip()

            if location == "Online Dealer":
                location = "Bucuresti"
            elif location == "Other Roles":
                location = "Bucuresti"
            elif location == "Bucharest":
                location = "Bucuresti"

            county = get_county_json(location)

            # print(update_location_if_is_county(counties=county, locations=location))
            # get jobs items from response
            job_list.append(Item(
                job_title=job.find("a").get_text(strip=True),
                job_link=job.find("a").get("href"),
                company="partnerd",
                country="România",
                county=county,
                city=location,
                remote=job_type,
            ).to_dict())

        if soup.find("div", id="show_more_button"):
            url  = "https://partnerd.teamtailor.com/jobs?page=2&query=&split_view=true"
        else:
            break

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
