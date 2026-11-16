"""Config for Dynamic Get Method -> For Json format!

Company ---> Freudenberg Performance Materials SRL
Link ------> https://jobs.freudenberg.com/Freudenberg/?company=FPM&location=RO

"""

import json

from __utils import Item, UpdateAPI


API_URL = "https://jobs.freudenberg.com/Freudenberg/api/json/?company=FPM&location=RO"


def _load_jobs():
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return {"jobs": []}

    for _ in range(3):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
                context = browser.new_context()
                response = context.request.get(API_URL, timeout=60000)
                text = response.text()
                browser.close()
            if text:
                return json.loads(text)
        except Exception:
            continue
    return {"jobs": []}


def scraper():
    """
    ... scrape data from Freudenberg Performance Materials SRL scraper.
    """
    json_data = _load_jobs()

    job_list = []
    for job in json_data["jobs"]:
        job_list.append(
            Item(
                job_title=job["jobtitle"],
                job_link=job["deepLink"],
                company="Freudenberg Performance Materials SRL",
                country="Romania",
                county="Brasov",
                city="Brasov",
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

    company_name = "Freudenberg Performance Materials SRL"
    logo_link = "https://www.freudenberg-pm.com/-/media/Images/Logos/FREUDENBERG_PERFORMANCE_MATERIALS.svg?h=48&w=294&la=en&hash=ACFC54066D4BB1FDBDAA4826B6F4A294"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
