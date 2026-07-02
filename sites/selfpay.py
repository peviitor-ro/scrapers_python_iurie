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
# Company ---> SelfPay
# Link ------> https://careers.smartrecruiters.com/SelfPay
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
    ... scrape data from SelfPay scraper.
    """
    soup = GetStaticSoup("https://careers.smartrecruiters.com/SelfPay")

    job_list = []
    for section in soup.find("div", class_="js-openings-load").find_all("section", class_="openings-section"):
        location = section.find("h3", class_="opening-title").text.split(', R')[0]
        county = get_county(location)
        for job in section.find_all("li", class_="opening-job"):
            job_list.append(Item(
                job_title=job.find("h4", class_="details-title").text,
                job_link=job.find("a", class_="link--block")["href"],
                company="SelfPay",
                country="România",
                county=county[0] if True in county else None,
                city='all' if True in county and county[0] != 'Bucuresti' else county[0],
                remote='remote' if job.find('i') else 'on-site',
            ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "SelfPay"
    logo_link = "https://selfpay.ro/wp-content/uploads/2018/04/selfpay_logo_site-03.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
