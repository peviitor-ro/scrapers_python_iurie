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
# Company ---> Concentrix
# Link ------> https://jobs.concentrix.com/job-search/?keyword=&country=Romania
#
#
from __utils import (
   
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
import  requests
from bs4 import BeautifulSoup


def scraper():
    """
    ... scrape data from Concentrix scraper.
    """
    payload={"action":"gd_jobs_query_pagination",
               "country":"Romania",
               "jobs_shown":0,
               "jobs_per_page":50
               }
   
    headers={
        "x-requested-with":"XMLHttpRequest"
    }
    url="https://jobs.concentrix.com/wp-admin/admin-ajax.php"
    responce=requests.post(url=url, data=payload, headers=headers)
    html=responce.json().get("data").get("output")
    soup=BeautifulSoup(html,'lxml')
    # print(responce)
    job_list = []
    for job in soup.find_all("div",attrs="job"):
        title=job.find("h3").text
        clean_title=title.split(' –')[0].split(" - ")[0]
        location=job.find("div", attrs="job-location").text.split(', R')[0]
        # change Bucharest to București
        if location=="Bucharest":
            location="București"
        #check if location is county 
        check_county=get_county(location)
        
        # get jobs items from response
        job_list.append(Item(
            job_title=clean_title,
            job_link=job.find("a")["href"],
            company="Concentrix",
            country="România",
            county = check_county[0] if True in check_county else None,
            city = 'all' if True in check_county and check_county[0]!='Bucuresti' else location ,
            remote = get_job_type(title),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Concentrix"
    logo_link = "https://jobs.concentrix.com/wp-content/themes/jobswh/img/logo-concentrix-color.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
