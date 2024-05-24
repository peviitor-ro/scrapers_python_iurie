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
# Company ---> Gameloft
# Link ------> https://careers.smartrecruiters.com/Gameloft/api/groups?page=0
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
    ... scrape data from Gameloft scraper.
    """
    soup = GetStaticSoup("https://careers.smartrecruiters.com/Gameloft/api/groups?page=0")

    job_list = []
    for job in soup.find_all("section",attrs="openings-section opening opening--grouped js-group"):
        if 'Bucharest' in job.find('h3', class_='opening-title title display--inline-block text--default').text:
            for j in job.find_all("li", attrs="opening-job job column wide-7of16 medium-1of2"):
                link = j.find('a', class_='link--block details')['href']
                title = j.find('h4', class_='details-title job-title link--block-target').text

                # get jobs items from response
                job_list.append(Item(
                    job_title=title, 
                    job_link=link,
                    company="Gameloft",
                    country="Romania",
                    county="București",
                    city="București",
                    remote="hybrid",
                ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Gameloft"
    logo_link = "https://www.gameloft.ro/wp-content/uploads/2017/05/logo_gameloft_black.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
