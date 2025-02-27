"""

 Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> breakpointit
Link ------> https://breakpointit-1655385323.teamtailor.com/jobs

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
    ... scrape data from breakpointit scraper.
    https://breakpointit-1655385323.teamtailor.com/jobs
    """
    soup = GetStaticSoup("https://breakpointit-1655385323.teamtailor.com/jobs")

    job_list = []
    for job in soup.find_all(
        "a",
        class_="flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg focus-visible-company focus-visible:rounded",
    ):

        job_type = job.find("div", class_="mt-1 text-md").text.strip()
        title = job.find(
            "span",
            class_="text-block-base-link sm:min-w-[25%] sm:truncate company-link-style hyphens-auto",
        ).text
        # get jobs items from response
        job_list.append(
            Item(
                job_title=title,
                job_link=job.get("href"),
                company="Breakpointit",
                country="România",
                county=get_county_json("Cluj-Napoca"),
                city="Cluj-Napoca",
                remote=get_job_type(job_type),
            ).to_dict()
        )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "breakpointit"
    logo_link = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/de4a3e93-31b3-4373-9d93-c193ee707218/original.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
