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
# Company ---> Expleo
# Link ------> https://careers-expleo-jobs.icims.com/jobs/search?ss=1&searchLocation=13526&mobile=false&width=1070&height=500&bga=true&needsRedirect=false&jan1offset=60&jun1offset=120
#
#
from __utils import (
    RequestsCustum,
    GetStaticSoup,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
from bs4 import BeautifulSoup
import requests

def scraper():
    """
    ... scrape data from Expleo scraper.
    """
    job_list = []
    headers = {'Cookie': 'icimsCookiesEnabledCheck=1; JSESSIONID=3DD6AAE2CBC007CE6B9E64F523DAF8C9'}
    payload = {}
    url="https://careers-expleo-jobs.icims.com/jobs/search?ss=1&searchLocation=13526&mobile=false&width=1070&height=500&bga=true&needsRedirect=false&jan1offset=60&jun1offset=120&in_iframe=1"
    
    response = requests.request("GET", url, headers=headers, data=payload)
    # response = RequestsCustum(url, headers=headers, payload=payload)
   
    soup = BeautifulSoup(response.text, 'html.parser')
    for job in soup.find_all('div', class_='row'):
        info_text = job.find('a')
        if info_text:
            link = job.find('a')['href']
            title = job.find('h3').text.strip()
            city = job.find('dd', class_='iCIMS_JobHeaderData').text.strip().split('-')[-1]
            # Find job_type
            spans = job.find_all('span')
            # Extract the content of the last <span>
            job_type = spans[-1].text.strip()
            if "Bucharest" in city:
                city="București"
            if "lasi" in city:
                city="Iasi"
    
            # get jobs items from response
            job_list.append(Item(
                job_title=title,
                job_link=link,
                company="Expleo",
                country="România",
                county=get_county_json(city),
                city=city,
                remote=job_type,
            ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Expleo"
    logo_link = "https://image.pitchbook.com/dYTzPN05fKU2JaRlSO8a5I1t1S91628514811898_200x200"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
