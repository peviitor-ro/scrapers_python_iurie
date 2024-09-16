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
# Company ---> Infotree Global Solutions
# Link ------> https://careereu.infotreeglobal.com/jobs?country=Romania&split_view=true&query=
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Infotree Global Solutions scraper.
    https://careereu.infotreeglobal.com/jobs?country=Romania&split_view=true&query=
    """
    soup = GetStaticSoup("https://careereu.infotreeglobal.com/jobs?country=Romania&split_view=true&query=")
    
    job_list = []
    for job in soup.find_all('a', class_="block h-full w-full hover:bg-company-primary-text hover:bg-opacity-3 overflow-hidden group"):
        
        data = job.find("div", class_="mt-1 text-md").text.strip()
        #extract job type from data
        job_type=get_job_type(data)
        
        location=job.find("div", class_="mt-1 text-md").text.strip()
        #find location and replace Bucharest with București
        location = "București" if "Bucharest" in location else location.split("·")[-1].strip().split(",")
        location = "all" if "Fully Remote" in location else location
        county = []
        
        if isinstance(location, list):
            for city in location:
                cities=get_county_json(city.strip())
                county+=cities
                county=list(set(county))
                
        else:
           county="all" if "all" in location else  get_county_json(location)
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("span", class_="text-block-base-link company-link-style").text,
            job_link=job.get("href"),
            company="Infotreeglobalsolutions",
            country="România",
            county=county,
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

    company_name = "Infotreeglobalsolutions"
    logo_link = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/388e65af-e792-4620-98f9-2291531833e9/original.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
