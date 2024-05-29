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
# Company ---> Bluewiresoftware
# Link ------> https://careers.smartrecruiters.com/BlueWireSoftware
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    get_county_json,
    Item,
    UpdateAPI,
)


def scraper():
    """
    scrape data from Bluewiresoftware scraper.
    """
    job_list = []
    loocation = ['Cluj-Napoca', 'București', 'Târgu Mureș']
    
    for city_locattion in loocation:
        
        soup = GetStaticSoup(f"https://careers.smartrecruiters.com/BlueWireSoftware?search={city_locattion}")
        #check if city_location is a county
        check_county = get_county_json(city_locattion if city_locattion != 'Târgu Mureș' else 'Targu-Mures' )
        
        for job in soup.find_all('li', attrs=('opening-job job column wide-7of16 medium-1of2')):
            title = job.find('h4', class_='details-title job-title link--block-target').text
            # get jobs items from response
            job_list.append(Item(
                job_title = title,
                job_link = job.find('a', class_='link--block details')['href'],
                company = 'Bluewiresoftware',
                country = 'România',
                county = check_county,
                city = city_locattion,
                remote = 'remote' if job.find('i') else get_job_type("hibrid") if title == "Infrastructure Engineer" else 'on-site',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Bluewiresoftware"
    logo_link = "https://c.smartrecruiters.com/sr-careersite-image-prod-dc5/5b7a6bb2e4b01c87868aa28a/6f824858-3319-4736-aa6a-e86f48f15345?r=s3-eu-central-1"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
