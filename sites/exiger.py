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
# Company ---> Exiger
# Link ------> https://boards.greenhouse.io/embed/job_board?for=exiger&b=https%3A%2F%2Fwww.exiger.com%2Fcareers%2F
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    get_county_json,
    Item,
    UpdateAPI,
)

def scraper():
    '''
    ... scrape data from Exiger scraper.
    '''
    soup = GetStaticSoup("https://boards.greenhouse.io/embed/job_board?for=exiger&b=https%3A%2F%2Fwww.exiger.com%2Fcareers%2F")

    job_list = []
    for job in soup.find_all('div', class_='opening'):
        
        location = job.find('span', class_='location').text
        
        if location.lower()=='bucharest':
            
            # get jobs items from response
            job_list.append(Item(
                job_title = job.find('a').text,
                job_link = job.find('a')['href'],
                company='Exiger',
                country='România',
                county = "Bucuresti",
                city="Bucuresti",
                remote  = "on-site",
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Exiger"
    logo_link = "https://www.exiger.com/wp-content/uploads/2023/04/logo_midnight@2x.png.webp"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
