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
# Company ---> Concentrix
# Link ------> https://jobs.concentrix.com/job-search/?keyword=&country=Romania
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
    ... scrape data from Concentrix scraper.
    """
    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"action\"\r\n\r\ngd_jobs_query_pagination\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"country[]\"\r\n\r\nRomania\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"jobs_shown\"\r\n\r\n0\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"jobs_per_page\"\r\n\r\n100\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"keyword\"\r\n\r\n\r\n-----011000010111000001101001--\r\n"
    soup = GetStaticSoup("https://jobs.concentrix.com/job-search/?keyword=&country=Romania")

    job_list = []
    for job in soup.find_all("div",attrs="job"):
        title=job.find("h3").text
        location=job.find("div", attrs="job-location").text.split(', R')[0]
        # change Bucharest to București
        if location=="Bucharest":
            location="București"
        #check if location is county 
        check_county=get_county(location)[0] if True in get_county(location)  else None
    
        # get jobs items from response
        job_list.append(Item(
            job_title=title,
            job_link=job.find("a")["href"],
            company="Concentrix",
            country="Romania",
            county = check_county,
            city = location if check_county==None else "all" ,
            remote = get_job_type(title),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Concentrix"
    logo_link = "https://jobs.concentrix.com/wp-content/themes/jobswh/img/logo-concentrix-color.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
