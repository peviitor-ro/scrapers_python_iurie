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
# Company ---> Kronospan
# Link ------> https://kronospan-candidate.talent-soft.com/job/list-of-jobs.aspx?page=1&LCID=1048
#
#
from lxml import etree
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)





def scraper():
    '''
    ... scrape data from Kronospan scraper.
    '''
    job_list = []
    page = 1
    flag = True
    romanians_cities=["Brasov","Sebes"]
    while flag:
        soup = GetStaticSoup(f"https://kronospan-candidate.talent-soft.com/job/list-of-jobs.aspx?page={page}&LCID=1048")         
        if len(jobs := soup.find_all('li',  attrs="ts-offer-list-item offerlist-item"))>1:
            for job in jobs:
                # location filter
                location_text = job.find('ul', class_='ts-offer-list-item__description')
                for location in location_text:
                    if location.text in romanians_cities:
                        # get jobs items from response
                        job_list.append(Item(
                            job_title=job.find("h3", attrs="ts-offer-list-item__title styleh3").text.strip(),
                            job_link="https://kronospan-candidate.talent-soft.com"+job.find("a")["href"],
                            company='Kronospan',
                            country="Romania", 
                            county=None,
                            city=location.text,
                            remote='on-site',
                        ).to_dict())
        else:
            flag=False
            break
        # increment page
        page += 1
        # time.sleep(1)

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Kronospan"
    logo_link = "https://logos-download.com/wp-content/uploads/2016/06/Kronospan_logo_blue_bg.png"

    jobs = scraper()
    print("job found:",len(jobs ))
    # uncomment if your scraper done
    # UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
