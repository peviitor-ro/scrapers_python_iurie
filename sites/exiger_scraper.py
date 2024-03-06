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
    Item,
    UpdateAPI,
)


'''
    
    + poti sa-i adaugi si custom_headers
    soup = GetStaticSoup(link, custom_headers)
    ... by default, custom_headers = None, dar in __utils ai un fisier
    default_headers.py unde poti sa-ti setezi headerele tale default.

    --------------IMPORTANT----------------
    La nivel de proiect, ca o variabila globala, este definit Session()!
    ... acest session inseamna ca orice clasa va putea folosi
    ... aceeasi sesiune, practic se va evita multiple requests;

    ########################################################################

    2) ---> get_county(nume_localitate) -> returneaza numele judetului;
    poti pune chiar si judetul, de exemplu, nu va fi o eroare.

    ########################################################################

    3) --->get_job_type(job_type: str) -> returneaza job_type-ul: remote,
    hybrid, on-site

    ########################################################################

    4) ---> Item -> este un struct pentru datele pe care le vom stoca in lista
    si, apoi, le vom trimite catre API.
    exemplu: job_list.append(Item(job_title="titlu_str",
                                    job_link="link",
                                    company="nume_companie",
                                    country="Romania",
                                    county="Judetul",
                                    city="Orasul",
                                    remote="remote, onsite sau hibryd"))

    ########################################################################

    5) ---> clasa UpdateAPI are doua metode:
    update_jobs(lista_dict_joburi) si update_logo(nume_companie, link_logo)

    UpdateAPI().update_jobs(company_name: str, data_jobs: list)
    UpdateAPI().update_logo(id_company: str, logo_link: str)

    ########################################################################
'''


def scraper():
    '''
    ... scrape data from Exiger scraper.
    '''
    soup = GetStaticSoup("https://boards.greenhouse.io/embed/job_board?for=exiger&b=https%3A%2F%2Fwww.exiger.com%2Fcareers%2F")

    job_list = []
    for job in soup.find_all('div', attrs='opening'):
        
        location = job.find('span', attrs= 'location').text
        #get_county  tuple with location Bucuresti
        county = get_county("Bucuresti") if location.lower() == 'bucharest' else None
        
        if location.lower() == 'bucharest':
            
            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('a').text,
                job_link= job.find('a')['href'],
                company='Exiger',
                country='România',
                county= county[0] if True in county else None,
                city='all' if True in county and county[0].lower() != 'bucuresti' else county[0],
                remote=get_job_type(''),
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
    # print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
