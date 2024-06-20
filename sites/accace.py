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
# Company ---> Accace
# Link ------> https://accace.ro/cariere/#oportunitati
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
    ... scrape data from Accace scraper.
    '''
    job_list = []
    data_loc_type = []
    
    jobs_type=["Remote","Hibrid","On-site"]
    for type in jobs_type:
        soup = GetStaticSoup(f"https://accace.ro/jobs/?_sfm_job_features_acc-jobs_work-mode={type}")
        data=soup.find("div",class_="oxy-dynamic-list acc-jobs-archive-repeater").find_all('a', class_="ct-link")
        
        for job in data:
            if len(job.contents)>0:
                title = job.find("span", attrs="ct-span").text.strip()
                link=job.get('href')
                
                # Extract location and job type from page
                location=job.find("div", class_="ct-code-block").text.split(', ')
                if len(location)>1:
                    location.remove("România")
                                
                # get jobs items from response
                job_list.append(Item(
                    job_title = title,
                    job_link = link,
                    company='Accace',
                    country='România',
                    county = get_county_json(location[0]),
                    city = 'all' if type.lower()=='remote' or location[0]=="România" else location,
                    remote=get_job_type(type) ,
                ).to_dict()) 

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Accace"
    logo_link = "https://www.movexstehovani.cz/wp-content/uploads/2018/09/LOGO_ACCACE_blue.png"

    jobs = scraper()
    print(len(jobs))
    
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
