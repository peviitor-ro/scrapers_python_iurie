#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> ALSO
# Link ------> https://www.also.com/ec/cms5/en_6000/6000/company/career/open-positions/jobs_json_4.json
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

    UpdateAPI().update_jobs(company_name: str, data_jobs: list)
    UpdateAPI().update_logo(id_company: str, logo_link: str)

    ########################################################################
'''


def scraper():
    '''
    ... scrape data from ALSO scraper.
    '''
    json_data = GetRequestJson("https://www.also.com/ec/cms5/en_6000/6000/company/career/open-positions/jobs_json_4.json")

    # read data from json_data and append it to job_list[]
    
    job_list = []
    for job in json_data['jobs']:
        if job['country'] == 'Romania': 
        # get jobs items from response
            job_list.append(Item(
                job_title=job['title'],
                job_link=job['url'],
                company='ALSO',
                country=job['country'],
                county= 'București' if get_county('București')[-1] == True else get_county('București')[0],
                city='București',
                remote = get_job_type(''),
            ).to_dict())

    return job_list

def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ALSO"
    logo_link = "https://private-user-images.githubusercontent.com/142620951/311528647-20fc0db4-8ca0-454d-80fb-5a2ee07a9799.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTAxNTQ0NjcsIm5iZiI6MTcxMDE1NDE2NywicGF0aCI6Ii8xNDI2MjA5NTEvMzExNTI4NjQ3LTIwZmMwZGI0LThjYTAtNDU0ZC04MGZiLTVhMmVlMDdhOTc5OS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMzExJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDMxMVQxMDQ5MjdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1jYTkwNjRjMTg0ZDI5NmM3OGFmZDdhMTdjOWU4YWZiMzg5ZmFlNjdiMmEzZTA0NzVjMmMwNjExNzI2MzUxM2EwJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.kUyvHe9BM4MNa4T9uL2hur1lxcYxkTaXB34IO5nA8oo"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
