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
# Company ---> Seimaf
# Link ------> https://www.seimaf.com/ro/ofertele-de-locuri-de-munca/?fwp_job_location=bucuresti-romania

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
    ... scrape data from Seimaf scraper.
    """
    soup = GetStaticSoup("https://www.seimaf.com/ro/ofertele-de-locuri-de-munca/?fwp_job_location=bucuresti-romania")

    job_list = []
    job_urgent=soup.find_all("article", attrs="card-jobcard-job--urgent highlighted-block")
    if job_urgent:
        for job in job_urgent:
            
            # get jobs items from response
            job_list.append(Item(
                job_title=job.find("h1", attrs="card-job__title").text.strip(),
                job_link=job.find("a")["href"],
                company="Seimaf",
                country="România",
                county="Bucuresti",
                city="Bucuresti",
                remote="on-site",
            ).to_dict()) 
       
    for job in soup.find_all("article",attrs="card-job"):
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h1", attrs="card-job__title").text.strip(),
            job_link=job.find("a")["href"],
            company="Seimaf",
            country="România",
            county="Bucuresti",
            city="Bucuresti",
            remote = "on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Seimaf"
    logo_link = "https://media.licdn.com/dms/image/C4D0BAQFBr5eOnAWpow/company-logo_200_200/0/1560859334430?e=2147483647&v=beta&t=bSgsiVGvV41-VRZZ_zPDuyQYq6BY0HfkG1w2eQ8SOcc"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
