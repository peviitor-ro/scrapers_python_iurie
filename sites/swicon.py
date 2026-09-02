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
# Company ---> Swicon
# Link ------> https://swicon.com/jobs
#
#
from __utils import (
    Item,
    UpdateAPI,
    GetStaticSoup,
)


def get_jobs_page():
    return GetStaticSoup("https://swicon.com/jobs")


def scraper():
    """
    ... scrape data from Swicon scraper.
    """
    soup = get_jobs_page()
    cards = soup.find_all("div", class_="job-card")

    job_list = []
    for card in cards:
        city = (card.get("data-city") or "").lower()
        if city != "bucharest":
            continue

        title_tag = card.find("a", class_="job-card-title")
        if not title_tag:
            continue

        job_title = title_tag.get_text(strip=True)
        job_link = title_tag.get("href", "")
        remote = (card.get("data-worktype") or "").capitalize()

        job_list.append(
            Item(
                job_title=job_title,
                job_link=job_link,
                company="Swicon",
                country="România",
                county="Bucuresti",
                city="Bucuresti",
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

    company_name = "Swicon"
    logo_link = "https://www.ejobs.ro/img/userCoverPhoto/f/5/f5e56fe04b0618594c10407feb11ecd4.jpg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
