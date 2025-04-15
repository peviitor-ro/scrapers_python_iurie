"""
Basic for scraping data from static pages

Company ---> expertware
Link ------> https://www.expertware.net/Careers

"""

import re
import json
from __utils import (
    GetDataCurl,
    Request,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


# Convert backtick strings to proper JSON strings and escape double quotes inside
def handle_backtick_strings(m):
    text = m.group(1)
    text = text.replace('"', '\\"')  # escape " inside the backtick content
    return f'"{text}"'


def scraper():
    """
    ... scrape data from expertware scraper.
    """
    job_list = []
    data = Request("https://www.expertware.net/Careers")

    # Extract the block containing the jobsList
    match = re.search(r"jobsList:\s*\[(.*?)\](?=\s*[,}])", data.text, re.DOTALL)

    if match:
        jobs_block = match.group(1)

        # Remove commented-out jobs
        jobs_block = re.sub(r"//\s*{.*?},?\n", "", jobs_block, flags=re.DOTALL)
        jobs_block = re.sub(r"^\s*//.*$", "", jobs_block, flags=re.MULTILINE)

        # Replace all single quotes with double quotes **before handling backticks**
        jobs_block = jobs_block.replace("'", '"')

        # Quote JS keys like img: → "img":
        jobs_block = re.sub(r"(\s*)(\w+):", r'\1"\2":', jobs_block)

        jobs_block = re.sub(r"`([^`]*)`", handle_backtick_strings, jobs_block)

        # Remove trailing commas before } or ]
        jobs_block = re.sub(r",(\s*[}\]])", r"\1", jobs_block)

        # Wrap and parse
        jobs_json = "[" + jobs_block.strip().rstrip(",") + "]"
        try:
            jobs = json.loads(jobs_json)

            for job in jobs:

                # get jobs items from response
                job_list.append(
                    Item(
                        job_title=job["title"],
                        job_link=f"https://www.expertware.net{job["link"]}",
                        company="expertware",
                        country="România",
                        county=get_county_json("Suceava"),
                        city="Suceava",
                        remote="on-site",
                    ).to_dict()
                )
        except json.JSONDecodeError as e:
            print("JSON decode failed:", e)

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "expertware"
    logo_link = "https://www.expertware.net/nowuiassets/img/logo_xblue_mobile.webp"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
