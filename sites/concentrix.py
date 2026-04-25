"""
Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> Concentrix
Link ------> https://jobs.concentrix.com/job-search/?keyword=&country=Romania

"""

import re

from __utils import GetDataCurl, Item, UpdateAPI, get_county_json, get_job_type


SEARCH_URL = "https://r.jina.ai/http://https://jobs.concentrix.com/job-search/?keyword=&country=Romania"


def _extract_jobs(search_text):
    match = re.search(r"## Search results \((\d+) jobs found\)(.*)Showing 1–10 of", search_text, re.S)
    if not match:
        return []

    results_block = match.group(2)
    return re.findall(
        r"\[(.*?)\s+###\s+(.*?)\s+(?:Apply with Concentrix!\s+)?([A-Za-zĂÂÎȘȘȚȚăâîșşțţ\-]+), Romania(?:\s+([A-Za-z]+))?\]\((https://jobs\.concentrix\.com/job/\?id=[^\)]+)\)",
        results_block,
    )


def scraper():
    """
    ... scrape data from Concentrix scraper.
    """
    search_text = GetDataCurl(SEARCH_URL)
    if not search_text:
        return []

    job_list = []
    for _category, title, city, language, link in _extract_jobs(search_text):
        if any(token in title for token in ["We're Concentrix", "Experience the power", "Our Risk and Compliance", "Success Program Skills Profile", "..."]):
            detail_text = GetDataCurl(f"https://r.jina.ai/http://{link}")
            detail_title_match = re.search(r"Home\]\([^\)]*\) » Job Details\s+\n\s+#\s+(.*?)\n", detail_text or "", re.S)
            if detail_title_match:
                title = detail_title_match.group(1).strip()

        city = "Bucuresti" if city in {"Bucharest", "Bucuresti", "București"} else city
        county = get_county_json(city)
        remote = get_job_type(f"{title} {language or ''}")

        job_list.append(
            Item(
                job_title=title.strip(),
                job_link=link,
                company="Concentrix",
                country="Romania",
                county=county,
                city=city,
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

    company_name = "Concentrix"
    logo_link = "https://jobs.concentrix.com/wp-content/uploads/2026/01/concentrix-logo-full-color.webp"

    jobs = scraper()
    print("jobs found:", len(jobs))
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
