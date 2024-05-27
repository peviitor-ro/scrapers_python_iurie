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
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Mediagalaxy scraper.
    """
    soup = GetStaticSoup("https://mediagalaxy.ro/cariere/")

    job_list = []
    county_finish=[]
    for job in soup.find_all("div",attrs="border rounded px-8"):
        title=job.find('h2', attrs="flex-shrink-0 mb-3 md:mb-0 md:w-64 md:pr-6 font-medium capitalize").text
        link=title.split()
        location=job.find('div', attrs="w-full mb-2 md:mb-0").text.split(':')[1].strip().split(',')
        location=[city.strip()for city in location]
        #check if location is county 
        county_finish=[city for city in location if True in get_county(city)]
        #remove all countyie from location
        only_city_location=list(set(location) - set(county_finish))
        
        # get jobs items from response
        job_list.append(Item(
            job_title=title.capitalize(),
            job_link="https://mediagalaxy.ro/cariere/#" + "-".join(link),
            company="Mediagalaxy",
            country="România",
            county = county_finish,
            city = only_city_location,
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
