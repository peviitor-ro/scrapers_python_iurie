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
# Company ---> BRINEL
# Link ------> https://www.brinel.ro/cariere#job-30
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


'''
    
    UpdateAPI().update_jobs(company_name: str, data_jobs: list)
    UpdateAPI().update_logo(id_company: str, logo_link: str)

    ########################################################################
'''


def scraper():
    '''
    ... scrape data from BRINEL scraper.
    '''
    soup = GetStaticSoup("https://www.brinel.ro/cariere#job-30")

    job_list = []
    for job in soup.find_all('div', attrs=('row align-items-center')):
        
        # Extrarct locaion from jobs
        city = job.find('span', attrs=('job--loc-type')).text.strip() if job.find('span', attrs=('job--loc-type')) != None else 'Cluj-Napoca'
        county = '' if city == None else get_county(city)
    
         # Find span element with class 'btn' and get 'data-bs-target' attribute
        span = job.find('span', class_='btn')
        if span:
            link = span.get('data-bs-target')

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h4').text.strip(),
            job_link='https://www.brinel.ro/cariere'+link,
            company='BRINEL',
            country='Romania',
            county = county[0] if True in county else None,
            city = 'all' if True in county and county[0].lower() != 'bucuresti' else city,
            remote = get_job_type(''),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "BRINEL"
    logo_link = "https://private-user-images.githubusercontent.com/153110403/311821470-497b197f-b552-4910-b69e-922893a61846.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTAxODM2MTIsIm5iZiI6MTcxMDE4MzMxMiwicGF0aCI6Ii8xNTMxMTA0MDMvMzExODIxNDcwLTQ5N2IxOTdmLWI1NTItNDkxMC1iNjllLTkyMjg5M2E2MTg0Ni5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMzExJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDMxMVQxODU1MTJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT02MDI0MmI5YjQxNDNhZTAwMzg5MDBjMjk4MGNlMjMzZDczZjMzZmViYWY2YjZmYjgyYzhmN2JkOWQwNWIxZTliJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.Vq0487fk_INq9cdMA3zC1EffJ5QRbePoBHfZ-5a_plw"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
