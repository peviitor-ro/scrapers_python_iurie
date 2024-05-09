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
# Company ---> Hennlich
# Link ------> https://www.hennlich.ro/cariera/toate-locurile-de-munca.html
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
    ... scrape data from Hennlich scraper.
    """
    soup = GetStaticSoup("https://www.hennlich.ro/cariera/toate-locurile-de-munca.html")

     
    job_list = []
  
    for job in soup.find_all("li",attrs="list_item list-group-item"):
        title=job.find('a').text
        link = "https://www.hennlich.ro/"+job.find('a')['href']
        
        if "Brașov" in title:
            location=["Brașov"]
        if "Turda" in title:
            location.append("Turda")
        else:
            location="Arad"
            
        #check if location is county
        # if "Brașov" in location:
        #     for county_location in  location:
        #         if True in get_county(county_location):
        #             countis.append(get_county(county_location)[0])
        #             location.remove("Brașov")
        # else:
        #     countis=get_county("Arad")[0] if True in get_county("Arad") else None
       
        # get jobs items from response
        job_list.append(Item(
            job_title=title,
            job_link=link,
            company="Hennlich",
            country="Romania",
            county=None,
            city=location,
            remote = get_job_type(""),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Hennlich"
    logo_link = "https://www.hennlich.ro/fileadmin/Public/images/hennlich_1.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
