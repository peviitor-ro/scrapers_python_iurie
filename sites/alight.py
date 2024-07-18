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
# Company ---> Alight
# Link ------> https://careers.alight.com/us/en/search-results?m=3&location=Virtual%2C%20Romania
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
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By

def scraper():
    """
    ... scrape data from Alight scraper using selenium.
    """
    job_list = []
    # instantiate options 
    options = webdriver.ChromeOptions() 
    # run browser in headless mode 
    options.headless = True 
    # instantiate driver 
    driver = webdriver.Chrome(service=Service( ChromeDriverManager().install()), options=options) 
    url = 'https://careers.alight.com/us/en/search-results?m=3&location=Virtual%2C%20Romania' 

    driver.get(url) 

    job_elements = driver.find_elements(By.CLASS_NAME,"jobs-list-item")
    
    for job in job_elements:
        link=job.find_element(By.TAG_NAME,"a").get_attribute("href")
        title=job.find_element(By.TAG_NAME,"h4").text
        # get jobs items from response
        job_list.append(Item(
            job_title=title,
            job_link=link,
            company="Alight",
            country="România",
            county="all",
            city="all",
            remote="remote",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Alight"
    logo_link = "https://cdn.phenompeople.com/CareerConnectResources/ALIGUS/en_us/mobile/assets/images/logo.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
