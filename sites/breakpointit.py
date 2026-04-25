"""

 Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> breakpointit
 Link ------> https://breakpointit.eu/careers

"""

from __utils import (
    GetRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from breakpointit scraper.
    https://breakpointit.eu/careers
    """
    json_data = GetRequestJson("https://breakpointit.eu/api/jobs")

    job_list = []
    for job in json_data:
        location = (job.get("location") or "").strip()
        if "romania" not in location.lower():
            continue

        remote = "remote" if "remote" in location.lower() else "on-site"

        job_list.append(
            Item(
                job_title=job.get("title"),
                job_link=f"https://breakpointit.eu/career/{job.get('slug')}",
                company="Breakpointit",
                country="Romania",
                county=get_county_json("Cluj-Napoca"),
                city="Cluj-Napoca",
                remote=remote,
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
    logo_link = "https://breakpointit.eu/images/logo_Breakpoint_sqare.webp"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
