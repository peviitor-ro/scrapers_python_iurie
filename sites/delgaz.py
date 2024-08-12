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
# Company ---> Delgaz
# Link ------> https://careers.eon.com/romania/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=&optionsFacetsDD_city=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield3=
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
    ... scrape data from Delgaz scraper.
    """
    remote_jobs=["German Speakers Interested in Accounting",
                 "Accounts Payable Associate (German Speaker)",
                 "Accounts Payable Associate (Hungarian Speaker, Fixed Term)",
                 "Accounts Payable Associate (Hungarian Speaker)",
                 "Fixed Assets Associate (Hungarian Speaker)",
                 "Technology Business Management Office Specialist",
                 "Accounts Payable Associate (German Speaker)"]
    job_list = []
    soup = GetStaticSoup("https://careers.eon.com/romania/search/?q=&sortColumn=referencedate&sortDirection=desc&startrow=1")
    pages=soup.find('li', text=lambda x: x and '2' in x).string  #soup.find("ul",{"class":"pagination"})[-1]

    for page in range(1,int(pages)+1):
        if page <=1:
            soup = GetStaticSoup(f"https://careers.eon.com/romania/search/?q=&sortColumn=referencedate&sortDirection=desc&startrow={page}")
        else:
            page=25
            soup = GetStaticSoup(f"https://careers.eon.com/romania/search/?q=&sortColumn=referencedate&sortDirection=desc&startrow={page}")
        
        for job in soup.find_all("tr",class_="data-row"):
            title=job.find("a",class_="jobTitle-link").text.strip()
            #extract location
            location = job.find("span",class_="jobLocation").text.strip().split(", RO")[0]
            #clean location typo
            location="Târgu-Mureș" if "Târgu Mureș"== location else "Piatra-Neamt" if location == "Piatra Neamț"  else location
           
            # get jobs items from response
            job_list.append(Item(
                job_title=title,
                job_link="https://careers.eon.com"+job.find("a",class_="jobTitle-link")["href"],
                company="Delgaz",
                country="România",
                county="Iași" if location=="Iași" else get_county_json(location),
                city=location,
                remote="hybrid" if title in remote_jobs  else "on-site",
            ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Delgaz"
    logo_link = "https://industrial-park.ro/wp-content/uploads/2019/05/delgaz-logo.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
