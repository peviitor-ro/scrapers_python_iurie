"""
 Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> Expressoft
Link ------> https://cariere.expressoft.ro/jobs

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
    ... scrape data from Expressoft scraper.
    """
    soup = GetStaticSoup("https://cariere.expressoft.ro/jobs")

    job_list = []
    for job in soup.find_all(
        "li",
        class_="transition-opacity duration-150 border rounded block-grid-item border-block-base-text border-opacity-15",
    ):

        if job.find("span", class_="inline-flex items-center gap-x-2"):
            job_type = job.find("span", class_="inline-flex items-center gap-x-2").text
        else:
            job_type = None

        # get jobs items from response
        job_list.append(
            Item(
                job_title=job.find("span", class_="text-block-base-link").text,
                job_link=job.find("a")["href"],
                company="Expressoft",
                country="România",
                county="București",
                city="București",
                remote=get_job_type(job_type) if job_type else "on-site",
            ).to_dict()
        )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Expressoft"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCSaup6KyvWosB-umVxAjMtgoub9RC_UA89DfFxqkd&s"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
