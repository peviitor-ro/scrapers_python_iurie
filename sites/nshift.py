""" 
Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> nShift
Link ------> https://careers.nshift.com/jobs?country=Romania&split_view=true&query=
"""

from __utils import (
    GetStaticSoup,
    get_county_json,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from nShift scraper.
    """
    soup = GetStaticSoup(
        "https://careers.nshift.com/jobs?country=Romania&split_view=true&query="
    )

    job_list = []
    for job in soup.select('a[href*="/jobs/"]'):
        data = [span.get_text(" ", strip=True) for span in job.find_all("span")]
        if len(data) < 6:
            continue

        title = data[0]
        location_text = data[3]
        job_type = data[5].strip().lower()

        if "," in location_text:
            city = "all"
            county = "all"
        else:
            city = "Bucuresti" if location_text == "Bucharest" else location_text
            county = get_county_json(city)
            county = county[0] if isinstance(county, list) and county else county

        # get jobs items from response
        job_list.append(
            Item(
                job_title=title,
                job_link=job.get("href"),
                company="nShift",
                country="România",
                county=county,
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

    company_name = "nShift"
    logo_link = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/1a33fc90-e83e-40e0-86a8-5daeb8a3db79/original.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
