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
# Company ---> EEUSoftware
# Link ------>  https://careers.smartrecruiters.com/EEUSoftware?remoteLocation=false
#
#
import time
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from EEUSoftware scraper.
    """
    job_list = []
    page='false'
    flag = True
    
    while flag:
        soup = GetStaticSoup(f"https://careers.smartrecruiters.com/EEUSoftware?remoteLocation={page}")
        if len(jobs := soup.find_all('li',  attrs='opening-job job column wide-7of16 medium-1of2'))> 1:
            for job in jobs:
                # get jobs items from response
                job_list.append(Item(
                    job_title = job.find('h4', attrs="details-title job-title link--block-target").text,
                    job_link = job.find('a')['href'],
                    company='EEUSoftware',
                    country='România',
                    county='București',
                    city='București',
                    remote = get_job_type(''),
                ).to_dict())
        else:
            flag = False
            break
        # increment page
        page='true'
        time.sleep(1)

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "EEUSoftware"
    logo_link = "https://www.eeusoft.ro/ro/wp-content/themes/eeutheme/images/logoEEU.svg"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
