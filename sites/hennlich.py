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
# Company ---> Hennlich
# Link ------> https://www.hennlich.ro/cariera/toate-locurile-de-munca.html
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Hennlich scraper.
    """
    soup = GetStaticSoup("https://www.hennlich.ro/cariera/toate-locurile-de-munca.html")
    job_list = []

    for job in soup.select("div.tx-jobapplications div.card"):
        title_tag = job.select_one("div.card-title a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")
        location_tag = job.find(string=lambda text: text and text.strip() == "Arad")
        location = location_tag.strip() if location_tag else "Arad"

        job_list.append(
            Item(
                job_title=title,
                job_link="https://www.hennlich.ro" + link,
                company="Hennlich",
                country="România",
                county=get_county(location)[0] if True in get_county(location) else None,
                city=location,
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

    company_name = "Hennlich"
    logo_link = "https://www.hennlich.ro/fileadmin/Public/images/hennlich_1.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
