#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Tec:agenc
# Link ------> https://tecss.bamboohr.com/careers/list

#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

'''
    Daca deja te-ai deprins cu aceasta formula de cod,
    atunci poti sterge acest comentariu din fisierul
    __create_scraper.py, din functia -> create_static_scraper_config <-

    Deci:
    ########################################################################

    1) --->  clasa GetRequestJson returneaza un obiect Json in urma unui
    GetRequest, direct in instanta.
    json_data = GetRequestJson(link) -> returneaza direct jsonul.
    Are default headers,

    dar daca vrei sa-i dai headers speciale, poti sa-i setezi cu
    json_data = GetRequestJson(link, custom_headers=headers -> new headers)

    --------------IMPORTANT----------------
    La nivel de proiect, ca o variabila globala, este definit Session()!
    ... acest session inseamna ca orice clasa va putea folosi
    ... aceeasi sesiune, practic se va evita multiple requests;

    ########################################################################

    2) ---> get_county(nume_localitat) -> returneaza numele judetului;
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

    UpdateAPI().update_jobs(data_jobs: list)
    UpdateAPI().update_logo(id_company: str, logo_link: str)

    ########################################################################
'''


def scraper():
    '''
    ... scrape data from Tec:agenc scraper.
    '''
    json_data = GetRequestJson("https://tecss.bamboohr.com/careers/list")

    job_list = []
    for job in json_data['result']:
        location  =  job['location']['city']
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job['jobOpeningName'],
            job_link="https://tecss.bamboohr.com/careers/"+job['id'],
            company="Tec:agenc",
            country="Romania",
            county=None,
            city=location,
            remote="hybrid" if job['locationType'] == '2' else "on-site",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Tec:agenc"
    logo_link = "logo_link"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
