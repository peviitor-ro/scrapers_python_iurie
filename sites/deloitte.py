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
# Company ---> Deloitte
# Link ------> https://apply.deloittece.com/en_US/careers/SearchJobs/?523=%5B5509%5D&523_format=1482&listFilterMode=1&jobRecordsPerPage=10&jobOffset=0
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
import math


def scraper():
    """
    ... scrape data from Deloitte scraper.
    https://apply.deloittece.com/en_US/careers/SearchJobs/?523=%5B5509%5D&523_format=1482&listFilterMode=1&jobRecordsPerPage=10&jobOffset=0
    """
    job_list = []
    location = []
    page = 0

    soup = GetStaticSoup(
        f"https://apply.deloittece.com/en_US/careers/SearchJobs/?523=%5B5509%5D&523_format=1482&listFilterMode=1&jobRecordsPerPage=10&jobOffset={page}")

    # extract from page "Displaying 1-10 of 102 results"
    total_jobs = soup.find('div', class_='list-controls__text__legend').text
    total_results = int(total_jobs.split('of')[-1].split()[0])
    # Calculate the number of pages
    pages = math.ceil(total_results / 10)

    for page in range(1, pages+1):

        for job in soup.find_all("div", class_="article__header__text"):

            span_elements = job.find_all('span')
            # extract data from span elements location and job type
            job_type_data = span_elements[-1].text.strip()
            location_data = span_elements[0].text.strip().split(
                '- R')[0].replace(',', '')
            # check if Bucharest and replace it with Bucuresti
            if 'Bucharest' in location_data:
                location_data = location_data.replace('Bucharest', 'București')
            location = location_data.split()
            # create a list of county base on city
            check_county = ["Iasi" if city == "Iasi" else get_county_json(city)[
                0] for city in location]

            # get jobs items from respons
            job_list.append(Item(
                job_title=job.find('a').text.strip(),
                job_link=job.find('a')['href'],
                company='Deloitte',
                country='România',
                county=check_county,
                city=location,
                remote=get_job_type(job_type_data),
            ).to_dict())

        # multiply with with 10 to increment page ofset number of jobs
        page *= 10
        soup = GetStaticSoup(
            f"https://apply.deloittece.com/en_US/careers/SearchJobs/?523=%5B5509%5D&523_format=1482&listFilterMode=1&jobRecordsPerPage=10&jobOffset={page}")

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Deloitte"
    logo_link = "https://www.bher.ca/sites/default/files/images/2022-03/Deloitte-Logo.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
