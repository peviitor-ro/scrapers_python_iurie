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
# Company ---> Olinio
# Link ------> https://careers.olinio.com.cy/jobs
#
#
from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Olinio scraper.
    """
    job_list = []
    page = 1

    while True:
        soup = GetStaticSoup(f"https://careers.olinio.com.cy/jobs?page={page}")
        jobs = soup.select('a[href*="/jobs/"]')
        if not jobs:
            break

        for job in jobs:
            data = [span.get_text(" ", strip=True) for span in job.find_all("span")]
            if len(data) < 4 or data[3] != "Bucharest":
                continue

            job_list.append(
                Item(
                    job_title=data[0],
                    job_link=job.get("href"),
                    company='Olinio',
                    country='România',
                    county='Bucuresti',
                    city='Bucuresti',
                    remote='on-site',
                ).to_dict()
            )

        page += 1

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Olinio"
    logo_link = "https://manatal-backend-public-assets.s3.amazonaws.com/media/career_portal_logo_direct_upload/fd9d1751-1e44-4977-a36a-353949d265b2_logo-light-olinio-retina.png"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
