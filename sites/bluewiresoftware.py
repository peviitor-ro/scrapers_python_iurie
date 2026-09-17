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
# Company ---> Bluewiresoftware
# Link ------> https://bluewiresoftware.careers-page.com/
#
#
import time

from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)

URL = "https://bluewiresoftware.careers-page.com/"


def run_with_retry(action, attempts=4):
    """
    Run the action, retrying on transient connection errors.
    """
    for attempt in range(attempts):
        try:
            return action()
        except Exception:
            if attempt == attempts - 1:
                print("Warning: request failed after retries.")
                return None
            time.sleep(2)


def scraper():
    """
    scrape data from Bluewiresoftware scraper.
    """
    soup = GetStaticSoup(URL)

    job_list = []
    for job in soup.find_all("article", class_="job-card"):
        title = job.find("h6", class_="job-title")
        link = job.find("a", class_="job-title-link")
        if not title or not link:
            continue

        job_list.append(Item(
            job_title=title.get_text(strip=True),
            job_link=URL.rstrip("/") + link["href"],
            company="Bluewiresoftware",
            country="România",
            county="Cluj",
            city="Cluj-Napoca",
            remote="remote",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Bluewiresoftware"
    logo_link = "https://d3neddlj774jsy.cloudfront.net/themes/media/clients/572262/9602280b-9497-4142-81c8-e86df159c55d/fd_branding_logo/2271a2a9-0cc4-42e7-a9d4-ed9744e431cdfd_branding_logo_header_1765973602814.png"

    jobs = run_with_retry(scraper) or []
    print(len(jobs))

    update_api = UpdateAPI()
    if jobs:
        run_with_retry(lambda: update_api.publish(jobs))
    else:
        print("No jobs to publish")
    run_with_retry(lambda: update_api.update_logo(company_name, logo_link))


if __name__ == '__main__':
    main()
