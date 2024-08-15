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
# Company ---> premierresearch
# Link ------> https://premier-research.com/our-company/careers/?locations=Romania
#
#
from __utils import (
    GetStaticSoup,
    RequestsCustumPost,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
from bs4 import BeautifulSoup

def scraper():
    """
    ... scrape data from Premier research scraper.
    """
    url = "https://premier-research.com/wp-admin/admin-ajax.php"

    payload = "action=load_jobs_by_locations&location=Romania&sterm="
    headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
            }
    responce = RequestsCustumPost(url=url, headers=headers, payload=payload)
    #convert responce to HTML format div class='\"job-title\"' to class="job-title"
    responce = responce.replace('\\', '')
    soup = BeautifulSoup(responce,'lxml')
   
    job_list = []
    for job in soup.find_all("li",class_="row no-gutters"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("div", class_="job-title").text,
            job_link="https://premier-research.com/our-company/careers/"+job.find("a", class_="btn btn-outline job-link")["href"],
            company="Premierresearch",
            country="România",
            county="Bucuresti",
            city="Bucuresti",
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "premierresearch"
    logo_link = "https://premier-research.com/wp-content/uploads/2019/04/Premier-Logo.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
