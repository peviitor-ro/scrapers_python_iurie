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
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
import time


def scraper():
    """
    ... scrape data from Olinio scraper.
    """
    job_list = []
    page = 1
    flag = True
    li_element = 'block-grid-item border border-block-base-text border-opacity-15 min-h-[360px] items-center justify-center rounded overflow-hidden relative z-career-job-card-image'
   
    while flag:
        soup = GetStaticSoup(f"https://careers.olinio.com.cy/jobs?page={page}")
        if len(jobs := soup.find_all('li',  attrs=li_element))> 1:
            for job in jobs:
                #extrract jobs only  from Bucharest
                location_span = job.find('span', string='Bucharest')
                if location_span:
                    job_type = job.find('span', attrs='inline-flex items-center gap-x-2')
                    title = job.find('span', attrs='text-block-base-link company-link-style').text
                    # get jobs items from response
                    job_list.append(Item(
                        job_title = title,
                        job_link = job.find('a')['href'],
                        company = 'Olinio',
                        country = 'Romania',
                        county = None,
                        city = 'Bucuresti',
                        remote = get_job_type('Hybrid Remote')if job_type else 'remote' if title == 'Database Analyst' else 'on-site' ,
                    ).to_dict())
        else:
            flag = False
            break
        # increment page
        page += 1
        time.sleep(1)
           
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
