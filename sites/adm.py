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
from __utils import (
    PostRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    '''
    ... scrape data from adm scraper.
    '''
    # https://sjobs.brassring.com/TGnewUI/Search/home/HomeWithPreLoad?partnerid=25416&siteid=5429&PageType=searchResults&SearchType=linkquery&LinkID=4393911#keyWordSearch=&Location%20Country=Romania
    url="https://sjobs.brassring.com/TgNewUI/Search/Ajax/MatchedJobs"
    payload = {
        "PartnerId": "25416",
        "SiteId": "5429",
        "Keyword": "",
        "Location": "",
        "KeywordCustomSolrFields": "JobTitle,Department,FORMTEXT8,FORMTEXT9",
        "LocationCustomSolrFields": "",
        "TurnOffHttps": False,
        "LinkID": "4393911",
        "EncryptedSessionValue": "^Wkx2c/3r4IeWLxJ7mJvxjZITgO6Sdyvz0/wOgWCIozYUhxDkJ4BI8HYl3TvFfFhtemtRrNpHTOUiZU3przMpaP2ibwiv/vPhPdlLtC_slp_rhc_jiH0=",
        "FacetFilterFields": {
            "Facet": [
            {
                "Name": "formtext10",
                "Options": [
                {
                    "OptionName": "Romania",
                    "OptionValue": "Romania",
                    "Selected": True
                }
                ],
                "AriaLabel_FilterResultsByFacet": "Filter search results by Location Country",
                "SelectedCount": 1
            }
            ]
        },
        "PowerSearchOptions": {
            "PowerSearchOption": [
            {
                "VerityZone": "JobTitle",
                "Type": "text",
                "Value": None
            },
            {
                "VerityZone": "FORMTEXT10",
                "Type": "single-select",
                "OptionCodes": []
            },
            {
                "VerityZone": "FORMTEXT9",
                "Type": "single-select",
                "OptionCodes": []
            },
            {
                "VerityZone": "FORMTEXT8",
                "Type": "single-select",
                "OptionCodes": []
            },
            {
                "VerityZone": "Department",
                "Type": "select",
                "OptionCodes": []
            },
            {
                "VerityZone": "AutoReq",
                "Type": "text",
                "Value": None
            },
            {
                "VerityZone": "LastUpdated",
                "Type": "date",
                "Value": None
            },
            {
                "VerityZone": "languagelist",
                "Type": "multi-select",
                "OptionCodes": []
            }
            ]
        },
        "SortType": "LastUpdated"
        }
    headers = {
    'Cookie': 'tg_session_25416_5429=^Wkx2c/3r4IeWLxJ7mJvxjZITgO6Sdyvz0/wOgWCIozYUhxDkJ4BI8HYl3TvFfFhtemtRrNpHTOUiZU3przMpaP2ibwiv/vPhPdlLtC_slp_rhc_jiH0=; tg_session=^Wkx2c/3r4IeWLxJ7mJvxjZITgO6Sdyvz0/wOgWCIozYUhxDkJ4BI8HYl3TvFfFhtemtRrNpHTOUiZU3przMpaP2ibwiv/vPhPdlLtC_slp_rhc_jiH0=; tg_rft=^KToplylAOAZwMsrLw0jJS7ut2pUA8AIUH60qzs/k6Of4sos+02Bekwv3q2sBzmSgnWCmUeptgicDzZbH6hWe5kztwNuQffQ8S37GgMkVYmg=; tg_rft_mvc=erQf2SkRgXiOYfKKUw_9rNWz1R3U1ZEzdtdiqNRTtCwnW1wQdcZ3wRXtX0J6X0HryisDuzRRnOL7K9_tHuVqrdsC8GorRI7vTsrXv9WJS0hPxfi3gd_7IaGmWDb-FVM1cMsRUQ2; TS014452f4=01c9c50cd316285eab958379e0e51d704455416de2ab8dd423eb718112cbeafd545ad28779f445e973860d6fa28f952be4ccc6b23a7aed3a1611a67e73e64db2e7995e063feabe9b13d86e6b9d5b7d191bfccac2ba53a9f513c2d35e8289eda45c697ef96c5a5039563173bab93cae831ea5919299; TS014452f4=01c9c50cd36bca5209a2705e0a3d331b1474996a9ae51e29b961969ac10cadc3c8d969a2d968578c615c2c1c88f8b8100a403b9321f6e70f8e1387421f1422d945073597d362c255d05ff04909fa21f08eaaf37ae8e5398a12cb5323f7833b8639bf9c748f03c9d7533e1292cde6ffa0461623ebc2',
    'RFT': 'T-3nJRzxuNs5F9cBKDBG2A675lB27vVCAJ-CzsPo4LJwdU8zGnPUeWoSkhHsyfaSW75lVWkWUAzvXFwrDNnh30ceKMf_pSsXqkDyY54Unl4TiPrJGuV0OAdXGo4QJ4rjp0nPuA2',
    'Content-Type': 'application/json'
    }

    
    json_data = PostRequestJson(url=url, custom_headers=headers, data_json=payload )

    job_list = []
    for job in json_data['Jobs']["Job"]:
        location= "Bucuresti" if"Bucharest" in job["Questions"][-2]["Value"] else job["Questions"][-2]["Value"]
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job["Questions"][-5]["Value"],
            job_link=job["Link"],
            company="Adm",
            country="România",
            county=get_county_json(location),
            city=location,
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
    logo_link = "https://extranet.e-adm.com/KenexaCandidateExport/Documents/Banner_Images/ADM_alternate_Logo.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
