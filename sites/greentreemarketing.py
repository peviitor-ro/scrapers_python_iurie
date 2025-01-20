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
# Company ---> GreenTreeMarketing
# Link ------> https://gtmarketing.ro/jobs/
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
    ... scrape data from GreenTreeMarketing scraper.
    """
    soup = GetStaticSoup("https://gtmarketing.ro/jobs/")

    job_list = []
    for job in soup.find_all("div", class_="list_item"):
        location = job.find(
            "ul", class_="list-unstyled").find_all('li')[1].text.strip().replace(", RO", "")
        city = "Bucuresti" if "Bucharest" in location else "all" if "Worldwide" in location else location
        county = "all" if "all" in city else get_county_json(city)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h4").text,
            job_link=job.find("a")["href"],
            company="Green Tree Marketing",
            country="România",
            county=county,
            city=city,
            remote="remote" if city == "all" else "on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Green Tree Marketing"
    logo_link = "https://gtmarketing.ro/wp-content/uploads/2022/09/logo-GTM-final.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
