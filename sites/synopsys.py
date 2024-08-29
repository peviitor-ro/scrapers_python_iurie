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
# Company ---> synopsys
# Link ------> https://careers.synopsys.com/search-jobs/results?RecordsPerPage=15&Location=Romania&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=4&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters;
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
    """
    ... scrape data from synopsys scraper.
    """
    job_list = []
    citis=["București","Cluj-Napoca","Iasi","Timișoara"]
    payload = {}
    headers = {
    'referer': 'https://careers.synopsys.com/search-jobs?k=&l=Romania&orgIds=44408'
    }
    url = "https://careers.synopsys.com/search-jobs/results?RecordsPerPage=15&Location=Romania&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=4&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters;"
    
    response = RequestsCustum(url=url, headers = headers, payload= payload)
    soup = BeautifulSoup(response.replace(r'\"', '"').replace(r'\r\n', '\n'), 'html.parser') 
  
    for job in soup.find_all("li",class_="search-results-list__list-item"):
        location=job.find("span",class_="job-location").text
        if "Multiple Locations"  in location:
            location=citis
        else:
            location=["București"]
            
        county=["Iasi" if city=="Iasi"  else get_county_json(city)[0] for city in location]
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h2").text,
            job_link="https://careers.synopsys.com"+job.find("a")["href"],
            company="synopsys",
            country="România",
            county=county,
            city=location,
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "synopsys"
    logo_link = "https://www.synopsys.com/content/experience-fragments/synopsys/en-us/global/eda/topnav/master/_jcr_content/root/topnav_copy.coreimg.svg/1706807034006/synopsys-logo-color.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
