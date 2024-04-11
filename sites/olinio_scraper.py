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


def scraper():
    """
    ... scrape data from Olinio scraper.
    """
    soup = GetStaticSoup("https://careers.olinio.com.cy/jobs")

    job_list = []
    for job in soup.find_all('li',  attrs='block-grid-item border border-block-base-text border-opacity-15 min-h-[360px] items-center justify-center rounded overflow-hidden relative z-career-job-card-image'):
        #extrract jobs only  from Bucharest
        location_span = job.find('span', string='Bucharest')
        if location_span:
            job_type = job.find('span', attrs='inline-flex items-center gap-x-2')
            # get jobs items from response
            job_list.append(Item(
                job_title = job.find('span', attrs='text-block-base-link company-link-style').text,
                job_link = job.find('a')['href'],
                company = 'Olinio',
                country = 'Romania',
                county = None,
                city = 'Bucuresti',
                remote = get_job_type('Hybrid Remote')if job_type else'on-site' ,
            ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Olinio"
    logo_link = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/4bb5fa99-79e7-48cc-ac02-faf0339cd2bf/original.png"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
