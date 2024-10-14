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
# Company ---> saltandpepper
# Link ------> https://saltandpepper.co/careers/
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


def scraper():
    """
    ... scrape data from saltandpepper scraper.
    """
    job_list = []
    url = "https://saltandpepper.co/careers/"

    payload = {}
    headers = {
        'Referer': 'https://saltandpepper.co/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    response = RequestsCustum(url=url, headers=headers, payload=payload)
    #parce string to a html object
    soup = BeautifulSoup(response,'html.parser')
    
    for job in soup.find_all("h3", class_="entry-title"):
        link = job.find("a")["href"]
        #open job position and extarct job type, location from job page
        data = RequestsCustum(url=link, headers=headers, payload=payload)
        data_job = BeautifulSoup(data,'html.parser')
        #find div with information from soup
        data_job.find_all("div", class_="et_pb_module")
        location_job_type = data_job.find("li", class_="p-small").text
        location  = location_job_type.split()[0]
        job_type = get_job_type(location_job_type)
        #append on-site option if location is present in location_job_type
        job_type.append("on-site") if "Cluj" in location_job_type else None
       
        # get jobs items from response
        job_list.append(Item(
            job_title=job.text,
            job_link=link,
            company="saltandpepper",
            country="România",
            county=get_county_json(location),
            city=location,
            remote=job_type,
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "saltandpepper"
    logo_link = "https://saltandpepper.co/wp-content/uploads/2020/05/logo-header2@2x.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
