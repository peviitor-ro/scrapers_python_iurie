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
# Company ---> Chorus
# Link ------> https://www.chorus.ro/job_list
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
    ... scrape data from Chorus scraper.
    """
    soup = GetStaticSoup("https://www.chorus.ro/Careers/Careers")

    job_list = []
    for job in soup.find_all('div', class_='card-body px-lg-4 d-flex flex-column justify-content-between'):
        
        location=job.find("h6", class_="card-subtitle mb-2 text-muted").text.strip()
        #clean location string
        if '(Se recruteaza si din:' in location:
            location=location.replace(" (Se recruteaza si din:", ",").replace("(", "").replace(")", "").strip()
        locations=location.strip().split(", ")

        #extract county for locations 
        check_county=[get_county_json(county) for county in locations ]
        clean_county=[item for sublist in check_county for item in sublist]
        unic_county=list(set(clean_county))
        
    
        # get jobs items from response
        job_list.append(Item(
            job_title = job.find("h5", class_="card-title primary-color-c").text,
            job_link = "https://www.chorus.ro"+job.find_all("a")[-1].get("href"),
            company = 'Chorus',
            country = 'România',
            county = unic_county,
            city = locations,
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Chorus"
    logo_link = "https://www.chorus.ro/images/logo.png?v=zXU74pBM8ngL6cEDeYM7AN61hnFBOVzAVCyZSWCxjng"

    jobs = scraper()
    print("jobs found",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
