"""
Basic for scraping data from static pages

Company ---> globallogic
Link ------> https://www.globallogic.com/career-search-page/page/1/?location=romania
"""

from __utils import (
    GetCustumRequest,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from globallogic scraper.
    """
    payload = {}
    headers = {
        "Cookie": "incap_ses_324_1279438=qRoLJ4SgbzegytCEVhR/BNKpIGcAAAAAVaTYjgljkvDdmpdyLc1wGw==; visid_incap_1279438=Ps0QFb7pRrW4mEDxOB/F+7+pIGcAAAAAQUIPAAAAAAAzzcXj1EATKZ9nhSZEWJp6; PHPSESSID=68hmh3g23aeflo3etkoov639l4; locations=romania; wordpress_google_apps_login=789a878c2075bd7d640fdc9992f86955"
    }

    job_list = []
    page = 1

    while True:
        if page == 1:
            url = "https://www.globallogic.com/career-search-page/?location=romania"
        else:
            url = f"https://www.globallogic.com/career-search-page/page/{page}/?location=romania"

        response = GetCustumRequest(url=url, payload=payload, headers=headers)
        jobs = response.find_all("a", class_="job_box")

        if not jobs:
            break

        for job in jobs:
            data = job.find("div", class_="top_area").text
            locations = [
                span.text.strip()
                for span in job.find_all("span", class_="job_location")
            ]

            if "Romania" in locations:
                if len(locations) > 1:
                    locations.remove("Romania")
                else:
                    locations = "all"

            if isinstance(locations, list) and "Bucharest" in locations:
                locations.remove("Bucharest")
                locations.append("Bucuresti")

            if "all" in locations:
                county = "all"
            else:
                county = [get_county_json(city) for city in locations]

            job_list.append(
                Item(
                    job_title=job.find("h4").text,
                    job_link=job.get("href"),
                    company="globallogic",
                    country="România",
                    county=county,
                    city=locations,
                    remote=get_job_type(data),
                ).to_dict()
            )

        page += 1

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "globallogic"
    logo_link = "https://www.globallogic.com/wp-content/uploads/2021/11/Wordmark.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
