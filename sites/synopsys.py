"""

Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> synopsys
Link ------> https://careers.synopsys.com/search-jobs/results?RecordsPerPage=15&Location=Romania&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=4&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters;

"""

from bs4 import BeautifulSoup
import requests
from __utils import (
    GetCustumRequestJson,
    GetRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from synopsys scraper.
    """
    job_list = []

    url = "https://careers.synopsys.com/search-jobs/results?RecordsPerPage=15&Location=Romania&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=4&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters;"
    payload = {}
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json; charset=utf-8",
        "cookie": "DefaultAsserted=Asserted; kndctr_96E61CFE53295EF20A490D45_AdobeOrg_identity=CiY2NzcyMjExMDk2MzU2MDc1OTAzNDIxOTg4MDg1ODM3MzQxMDkwMlIRCKOKnpfUMhgBKgRJUkwxMAGgAa6KnpfUMrABAPABo4qel9Qy; kndctr_96E61CFE53295EF20A490D45_AdobeOrg_cluster=irl1; AMCV_96E61CFE53295EF20A490D45%40AdobeOrg=MCMID|67722110963560759034219880858373410902; OptanonConsent=isIABGlobal=false&datestamp=Wed+Feb+26+2025+16%3A37%3A04+GMT%2B0100+(Central+European+Standard+Time)&version=6.27.0&hosts=&consentId=9546cf6b-0b8a-40da-b32e-e18be2d1f042&interactionCount=0&landingPath=https%3A%2F%2Fcareers.synopsys.com%2Fsearch-jobs%3Fk%3D%26l%3DRomania%26orgIds%3D44408&groups=C0001%3A1%2CC0003%3A0%2CC0002%3A0%2CC0004%3A0",
        "priority": "u=1, i",
        "referer": "https://careers.synopsys.com/search-jobs?k=&l=Romania&orgIds=44408",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    response = GetCustumRequestJson(url, headers=headers, payload=payload)

    soup = BeautifulSoup(response["results"], "html.parser")

    for job in soup.find_all("li", class_="search-results-list__list-item"):
        location = job.find("span", class_="job-location").text.split(",")[0]

        # get jobs items from response
        job_list.append(
            Item(
                job_title=job.find("h2").text,
                job_link="https://careers.synopsys.com" + job.find("a")["href"],
                company="synopsys",
                country="România",
                county=get_county_json(location),
                city=location,
                remote="on-site",
            ).to_dict()
        )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "synopsys"
    logo_link = "https://www.synopsys.com/content/experience-fragments/synopsys/en-us/global/eda/topnav/master/_jcr_content/root/topnav_copy.coreimg.svg/1706807034006/synopsys-logo-color.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
