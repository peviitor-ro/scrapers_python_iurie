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
# Company ---> luxoft
# Link ------> https://career.luxoft.com/jobs?keyword=&country[]=Romania&perPage=120
#
#
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
    ... scrape data from luxoft scraper.
    """
    soup = GetStaticSoup(
        "https://career.luxoft.com/jobs?keyword=&country[]=Romania&perPage=120")

    job_list = []
    for job in soup.find_all("a", class_="jobs__list__job"):
        city = job.find("p", class_="body-s-regular").text.strip()

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find(
                "p", class_="body-m-regular text-dark-gray").text.strip(),
            job_link="https://career.luxoft.com"+job.get("href"),
            company="luxoft",
            country="România",
            county="București" if "Bucharest" in city else "all",
            city="București" if "Bucharest" in city else "all",
            remote=get_job_type(city),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "luxoft"
    logo_link = "https://s.dou.ua/CACHE/images/img/static/companies/Luxoft_Purple_RGB/b0bd318ade945671cd9b7d6d1c79191a.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
