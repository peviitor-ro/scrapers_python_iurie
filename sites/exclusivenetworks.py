"""

 Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> Exclusive Networks Romania
Link ------> https://www.exclusive-networks.com/ro/about-exclusive-networks/careers/

"""

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
    ... scrape data from Exclusive Networks Romania scraper.
    """
    soup = GetStaticSoup(
        "https://www.exclusive-networks.com/ro/about-exclusive-networks/careers/"
    )

    job_list = []
    for job in soup.find_all("a", class_="job-link-box modified"):
        location = job.find("p").find("span").text
        if location =="Bucharest":
            location = "Bucuresti"

        # get jobs items from response
        job_list.append(
            Item(
                job_title=job.find("h2", class_="h4").text,
                job_link=job.get("href"),
                company="Exclusive Networks Romania",
                country="România",
                county=get_county_json(location),
                city=location,
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

    company_name = "Exclusive Networks Romania"
    logo_link = "https://www.immajg-consult.fr/wp-content/uploads/2015/03/Exclusive-network.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
