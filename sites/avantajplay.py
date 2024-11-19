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
# Company ---> AvantajPlay
# Link ------> https://www.avantajplay.ro/vacancies/
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from AvantajPlay scraper.
    """
    soup = GetStaticSoup("https://www.avantajplay.ro/vacancies/")

    job_list = []
    for job in soup.find_all('div', class_=('n-vacancies-cards')):
        title = job.find('div', class_="n-vacancies-cc-title").find("h3").text
        # get jobs items from response
        job_list.append(Item(
            job_title=title,
            job_link=job.find('a', class_="n-vacancies-card")['href'],
            company='Avantajplay',
            country='România',
            county="Brașov",
            city="Brașov",
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Avantajplay"
    logo_link = "https://www.avantajplay.ro/wp-content/uploads/2024/07/logo2.svg"

    jobs = scraper()
    print("Jobs found", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
