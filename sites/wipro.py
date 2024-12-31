#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> wipro
# Link ------> https://careers.wipro.com/api/jobs?location=Romania
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
    GetStaticSoup,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from wipro scraper.
    https://careers.wipro.com/search/?q=&locationsearch=Romania
    '''
    job_list = []
    
    pages = [1, 25]
    for page in pages:
        soup = GetStaticSoup(f"https://careers.wipro.com/search/?q=&locationsearch=Romania&startrow={page}")

        data = soup.find_all("tr", class_="data-row")
        if data:
            for job in data:
                location = job.find("span",  class_="jobLocation").text.strip().split(", R")[0]
                city = "Bucuresti" if "Bucharest" in location else location
                
                # get jobs items from response
                job_list.append(Item(
                    job_title=job.find("a",  class_="jobTitle-link").text,
                    job_link="https://careers.wipro.com"+job.find("a",  class_="jobTitle-link")["href"],
                    company="wipro",
                    country="România",
                    county=get_county_json(city),
                    city=city,
                    remote="on-site",
                ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "wipro"
    logo_link = "https://cms.jibecdn.com/prod/wipro/assets/HEADER-NAV_LOGO-en-us-1698423772812.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
