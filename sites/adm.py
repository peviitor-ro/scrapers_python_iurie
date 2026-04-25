#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> adm
# Link ------> https://sjobs.brassring.com/TgNewUI/Search/Ajax/MatchedJobs
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
import html
import re

import requests

from __utils import Item, UpdateAPI, get_county_json


SEARCH_URL = "https://sjobs.brassring.com/TGnewUI/Search/home/HomeWithPreLoad?partnerid=25416&siteid=5429&PageType=searchResults&SearchType=linkquery&LinkID=4393911#keyWordSearch=&Location%20Country=Romania"
MATCHED_JOBS_URL = "https://sjobs.brassring.com/TgNewUI/Search/Ajax/MatchedJobs"


def _get_question_value(job, question_name):
    for question in job.get("Questions", []):
        if question.get("QuestionName") == question_name:
            return question.get("Value")
    return None


def _build_session_data(page_text):
    rft_match = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', page_text)
    encrypted_match = re.search(r'EncryptedSessionValue\\&quot;:\\&quot;([^\"]+?)\\&quot;', page_text)

    if not rft_match or not encrypted_match:
        return None, None

    return rft_match.group(1), html.unescape(encrypted_match.group(1))

def scraper():
    '''
    ... scrape data from adm scraper.
    '''
    job_list = []
    session = requests.Session()
    response = session.get(SEARCH_URL, timeout=30)
    if response.status_code != 200:
        response.close()
        return job_list

    rft, encrypted_session_value = _build_session_data(response.text)
    response.close()
    if not rft or not encrypted_session_value:
        return job_list

    payload = {
        "PartnerId": "25416",
        "SiteId": "5429",
        "Keyword": "",
        "Location": "",
        "KeywordCustomSolrFields": "JobTitle,Department,FORMTEXT8,FORMTEXT9",
        "LocationCustomSolrFields": "",
        "TurnOffHttps": False,
        "LinkID": "4393911",
        "EncryptedSessionValue": encrypted_session_value,
        "FacetFilterFields": {
            "Facet": [
                {
                    "Name": "formtext10",
                    "Options": [
                        {
                            "OptionName": "Romania",
                            "OptionValue": "Romania",
                            "Selected": True,
                        }
                    ],
                    "AriaLabel_FilterResultsByFacet": "Filter search results by Location Country",
                    "SelectedCount": 1,
                }
            ]
        },
        "PowerSearchOptions": {
            "PowerSearchOption": [
                {"VerityZone": "JobTitle", "Type": "text", "Value": None},
                {"VerityZone": "FORMTEXT10", "Type": "single-select", "OptionCodes": []},
                {"VerityZone": "FORMTEXT9", "Type": "single-select", "OptionCodes": []},
                {"VerityZone": "FORMTEXT8", "Type": "single-select", "OptionCodes": []},
                {"VerityZone": "Department", "Type": "select", "OptionCodes": []},
                {"VerityZone": "AutoReq", "Type": "text", "Value": None},
                {"VerityZone": "LastUpdated", "Type": "date", "Value": None},
                {"VerityZone": "languagelist", "Type": "multi-select", "OptionCodes": []},
            ]
        },
        "SortType": "LastUpdated",
    }
    headers = {
        "Content-Type": "application/json",
        "RFT": rft,
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://sjobs.brassring.com",
        "Referer": SEARCH_URL,
    }
    jobs_response = session.post(MATCHED_JOBS_URL, json=payload, headers=headers, timeout=30)
    if jobs_response.status_code != 200:
        jobs_response.close()
        return job_list

    json_data = jobs_response.json()
    jobs_response.close()

    for job in (json_data.get("Jobs") or {}).get("Job", []):
        country = (_get_question_value(job, "formtext10") or "").strip()
        if country.lower() != "romania":
            continue

        location = (_get_question_value(job, "formtext8") or "").strip()
        location = "Bucuresti" if location == "Bucharest" else location
        county = "all" if not location else get_county_json(location)

        job_list.append(Item(
            job_title=_get_question_value(job, "jobtitle"),
            job_link=job.get("Link"),
            company="Adm",
            country="Romania",
            county=county,
            city=location or "all",
            remote="on-site",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Adm"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/3/36/Archer_Daniels_Midland_logo.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
