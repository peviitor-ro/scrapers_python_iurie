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
# Company ---> Mediagalaxy
# Link ------> https://mediagalaxy.ro/cariere/
#
#
from bs4 import BeautifulSoup
from __utils import (
    RequestsCustum,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """ scrape data from Mediagalaxy scraper """
    
    url = "https://mediagalaxy.ro/cariere/"

    payload = {}
    headers = {
            'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
            }
    data = RequestsCustum(url, headers, payload)
    # transfom text responce in soup object
    soup =  BeautifulSoup(data, 'lxml')

    job_list = []
    for job in soup.find_all("div",class_="border rounded px-8"):

        title=job.find('h2', class_="flex-shrink-0 mb-3 md:mb-0 md:w-64 md:pr-6 font-medium capitalize").text
        link=title.replace(" ","-")
        location=job.find('div', class_="w-full mb-2 md:mb-0").text.split(':')[1].strip().split(', ')
        county_finish=["Cluj"if city =="Cluj" else get_county_json(city)[0] for city in location]
       
        # get jobs items from response
        job_list.append(Item(
            job_title=title.capitalize(),
            job_link="https://mediagalaxy.ro/cariere/#" + link,
            company="Mediagalaxy",
            country="România",
            county = county_finish,
            city = location,
            remote = "on-site",     
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Mediagalaxy"
    logo_link = "https://bucurestimall.ro/wp-content/uploads/2016/12/MediaGalaxy.jpg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
