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
# Company ---> hirschmann-automotive
# Link ------> https://career.hirschmann-automotive.com/en/all-jobs?tx_site_jobapi%5Bcontroller%5D=Job&type=1598607815
#
#
from __utils import (
    PostCustumRequest,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
from bs4 import BeautifulSoup


def scraper():
    """
    ... scrape data from hirschmann-automotive scraper.
    https://career.hirschmann-automotive.com/en/all-jobs
    """
    url = "https://career.hirschmann-automotive.com/en/all-jobs?tx_site_jobapi%5Bcontroller%5D=Job&type=1598607815"

    payload = {'tx_site_jobapi[__trustedProperties]': '{"demand":{"jobType":1,"location":1,"limit":1,"offset":1},"detailPage":1,"cid":1}0130b1fbf738e4ecd2c007cb2b8264e40a735521',
               'tx_site_jobapi[demand][location]': '37',
               'tx_site_jobapi[detailPage]': '2560',
               'tx_site_jobapi[cid]': '2119'}

    headers = {
        'referer': 'https://career.hirschmann-automotive.com/en/all-jobs'
    }
    data = PostCustumRequest(url=url, payload=payload, headers=headers)

    job_list = []
    for job in data.find_all("li"):
        city = job.find_all(
            'p')[-1].get_text().split("-")[0].strip().replace(" ", "-")

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h3").text,
            job_link="https://career.hirschmann-automotive.com" +
            job.find("a").get("href"),
            company="hirschmann-automotive",
            country="România",
            county=get_county_json(city),
            city=city,
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "hirschmann-automotive"
    logo_link = "https://www.aki-gmbh.com/wp-content/uploads/logo-hirschmann-automotive.jpg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
