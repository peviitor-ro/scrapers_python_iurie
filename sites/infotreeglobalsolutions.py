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
    """
    soup = GetStaticSoup("https://careereu.infotreeglobal.com/jobs?country=Romania&split_view=true&query=")
    job_block=soup.find("ul", class_="block-grid")
    job_list = []
    for job in soup.find_all('a', class_="block h-full w-full hover:bg-company-primary-text hover:bg-opacity-3 overflow-hidden group"):
        #find location and replace Bucharest with București
        location=job.find("div", class_="mt-1 text-md").find('span').text
        location="București" if "Bucharest" in location else location
        #find job type if presnet or job_type on-site
        job_type=job.find("span", class_="inline-flex items-center gap-x-2")
        job_type=job_type.text.strip().lower().split() if job_type else "on-site"
    
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("span", class_="text-block-base-link company-link-style").text,
            job_link=job.get("href"),
            company="Infotreeglobalsolutions",
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

    company_name = "Infotreeglobalsolutions"
    logo_link = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/388e65af-e792-4620-98f9-2291531833e9/original.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
