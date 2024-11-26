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
# Company ---> nShift
# Link ------> https://careers.nshift.com/jobs?country=Romania&split_view=true&query=
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from nShift scraper.
    """
    soup = GetStaticSoup(
        "https://careers.nshift.com/jobs?country=Romania&split_view=true&query=")

    job_list = []
    for job in soup.find_all("a", class_="block h-full w-full hover:bg-company-primary-text hover:bg-opacity-3 overflow-hidden group"):
        job_type = job.find(
            "span", class_="inline-flex items-center gap-x-2").text.strip()
        # Extract the location from div
        data = job.find_all("span")
        if len(data) > 3:
            if "Multiple locations" in data[3]:
                location = ["Brașov", "București", "Cluj-Napoca"]
            else:
                location = "București" if "Bucharest" in data[3].text else None
        # get county for city
        county = "București" if location == "București" else [
            get_county_json(county)[0] for county in location]

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find(
                "span", class_="text-block-base-link company-link-style").text,
            job_link=job.get("href"),
            company="nShift",
            country="România",
            county=county,
            city=location,
            remote=get_job_type(job_type),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "nShift"
    logo_link = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/1a33fc90-e83e-40e0-86a8-5daeb8a3db79/original.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
