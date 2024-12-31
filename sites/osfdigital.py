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
# Company ---> OSFDIGITAL
# Link ------> https://osf.digital/careers/jobs?location=romania
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


def scraper():
    """
    ... scrape data from OSFDIGITAL scraper.
    """
    url  ="https://osf.digital/careers/jobs?location=romania"
    payload = "scController=OsfCommerceJob&scAction=GetItems&parameter=request&__RequestVerificationToken=l4mKbmE0X24D5hMK9zgq7soys2c1zmQ6oFmDl9ulml62jrcH5gt-RYlFjAn9Z1uHi78t5jCZkQD2lzOJcZxup10p7Pc1"
    headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': 'https://osf.digital/careers/jobs?location=romania'
        }

    responce = PostCustumRequest(url=url, payload= payload, headers= headers)

    job_list = []
    
    for job in  responce.find_all("div",class_="section-positions section-border"):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("a").text.strip(),
            job_link="https://osf.digital"+job.find("a").get("href"),
            company="OSF DIGITAL",
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

    company_name = "OSF DIGITAL"
    logo_link = "https://osf.digital/library/media/osf/digital/common/header/osf_digital_logo.svg?h=60&la=en&w=366&hash=5FF21BA406E10D94D9778FA8A3A8AEC43C247D2B"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
