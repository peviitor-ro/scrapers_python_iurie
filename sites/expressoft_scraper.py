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
# Company ---> Expressoft
# Link ------> https://expressoft.ro/cariere/
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
    '''
    ... scrape data from Expressoft scraper.
    '''
    soup = GetStaticSoup("https://expressoft.ro/cariere/")

    job_list = []
    for job in soup.find_all('div', attrs='accordion-item job'):
        
        finish_location = get_county(location =  "București")
        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('div', attrs='job__title accordion-title').text,
            job_link = job.find('a', class_='btn btn--secondary--solid')['href'],
            company='Expressoft',
            country='Romania',
            county = finish_location[0] if True in finish_location else None,
            city='all' if True  in finish_location and finish_location[0] != 'Bucuresti' else finish_location[0],
            remote=get_job_type(''),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Expressoft"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCSaup6KyvWosB-umVxAjMtgoub9RC_UA89DfFxqkd&s"

    jobs = scraper()
    # print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
