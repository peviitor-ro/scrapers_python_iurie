"""

 Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> Napa
Link ------> https://jobs.napa.fi/jobs

"""
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Napa scraper.
    """
    soup = GetStaticSoup(
        "https://jobs.napa.fi/jobs?location=NAPA+Romania&split_view=true&query="
    )

    job_list = []
    for job in soup.find_all("li", class_="w-full"):
        title = job.find(
            "span",
            class_="text-block-base-link sm:min-w-[25%] sm:truncate company-link-style hyphens-auto",
        ).text
        # get jobs items from response
        job_list.append(
            Item(
                job_title=title,
                job_link=job.find("a")["href"],
                company="Napa",
                country="România",
                county="Galati",
                city="Galati",
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

    company_name = "Napa"
    logo_link = "https://i.vimeocdn.com/portrait/30394561_640x640"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
