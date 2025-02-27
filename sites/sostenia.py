"""
Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> Sostenia
Link ------> https://www.sostenia.ro/en/jobs

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
    ... scrape data from Sostenia scraper.
    """
    soup = GetStaticSoup("https://www.sostenia.ro/en/jobs")

    job_list = []
    data = soup.find_all("a", class_="link-decoration-none")
    for job in data:
        title = job.find("h3", class_="text-secondary mt0 mb4").text.strip()
        link = "https://www.sostenia.ro/" + job.get("href")
        # Find all <li> elements that contain "remote" or "hibrid"
        result = [
            li.get_text(strip=True)
            for li in job.find_all("li")
            if "remote" in li.text.lower()
            or "hibrid" in li.text.lower()
            or "hybrid" in li.text.lower()
            or "remote/hybrid" in li.text.lower()
        ]
        job_type = get_job_type(result[0]) if result else "hybrid"
        # get jobs items from response
        job_list.append(
            Item(
                job_title=title,
                job_link=link,
                company="Sostenia",
                country="România",
                county="București",
                city="București",
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

    company_name = "Sostenia"
    logo_link = (
        "https://www.sostenia.ro/web/image/website/1/logo/Sostenia?unique=6994ba0"
    )

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
