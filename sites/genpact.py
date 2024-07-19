#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Genpact
# Link ------> https://www.genpact.com/index.php?p=actions/taleo-scraper/a-p-i/search
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

import requests
import re
def scraper():
    '''
    ... scrape data from Genpact scraper.
    '''
    job_list = []
    url = "https://www.genpact.com/index.php?p=actions/taleo-scraper/a-p-i/search"
    headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': '__cf_bm=yt7AWNsZMauZxjVLEWx0RI5sjMrLYzmRPJCOqNJxTiE-1721387771-1.0.1.1-rnhDh_s.yz4eaQkdhQ8IC9.8.HuiF0dBV6R0lNrQEZ0eG9Fsrm9st3ESmos17Y_VqtPBYKENcJohdaspYPx6Jg; _vwo_uuid_v2=D2C0586A86C3B3C6FF2C9D06EDF2BCA5E|229b2a71d21676630f388f0c6014ee32; _vwo_uuid=D2C0586A86C3B3C6FF2C9D06EDF2BCA5E; _vwo_sn=0%3A1%3A%3A%3A1; _uetsid=4dc0fc9045c011ef952e63427a2e94ab; _uetvid=4dc13fe045c011efb9d68303c5137813; OptanonConsent=isGpcEnabled=1&datestamp=Fri+Jul+19+2024+13%3A16%3A11+GMT%2B0200+(Central+European+Summer+Time)&version=202404.1.0&browserGpcFlag=1&isIABGlobal=false&hosts=&consentId=da5c348c-b57f-48d3-9ddf-13eca15a392f&interactionCount=0&isAnonUser=1&landingPath=https%3A%2F%2Fwww.genpact.com%2Fcareers%2Fjob-search%3Fkeyword%3D%26submit%3D&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0005%3A0; PRODUCTION_GENPACT_2022=e13b262529770e61e8457a4980aff8967996458b12157ad8c106e06072e08568a%3A2%3A%7Bi%3A0%3Bs%3A23%3A%22PRODUCTION_GENPACT_2022%22%3Bi%3A1%3Bs%3A40%3A%220X5sHLJ79NfzGu12PZwuVJ18gQisulcu7tSOSXOt%22%3B%7D; _vis_opt_s=1%7C; _vis_opt_test_cookie=1; _hjSessionUser_2455770=eyJpZCI6IjhhMmViZTRmLTBmNDktNWJkNy05OWVlLWU0OGQ2ODcwZTc5ZiIsImNyZWF0ZWQiOjE3MjEzODc3NzE0MzEsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_2455770=eyJpZCI6Ijg4MGQ3YzFmLTFiNzktNGEwNC04ZWY3LTY0M2Q3NDY1ZGRkYSIsImMiOjE3MjEzODc3NzE0MzMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _vwo_ds=3%3At_0%2Ca_0%3A0%241721387771%3A51.82812477%3A%3A%3A3_0%2C1_0%3A0; __cf_bm=2Y3GBO_yDogTwvh.r8IGzuAqyucIXRz_cvhPoxl2tgM-1721388555-1.0.1.1-l_l584Y.8Ny7YEVLnDhMwEFRVvtOZRE2Fg0zkZCy_hRswodjqC9Dyx3WLKewjaDQXdIXmz55HwL7tGRKuVRnQg; PRODUCTION_GENPACT_2022=24be91843fb5aea122cd029affe2e11890c2594efd61218e37c56b83690120e5a%3A2%3A%7Bi%3A0%3Bs%3A23%3A%22PRODUCTION_GENPACT_2022%22%3Bi%3A1%3Bs%3A40%3A%22U2c48F-mmDoopnBvbqXw_tunrW93M1jMM_ve6Bo2%22%3B%7D',
                'origin': 'https://www.genpact.com',
                'priority': 'u=1, i',
                'referer': 'https://www.genpact.com/careers/job-search?keyword=&submit=',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
                }
    page = 1
    for page in range(18):
        payload = f'PRODUCTION_GENPACT_2022=opONusKErFMggsBdND3Fh4AnBnZgI8ZhmJcMZZLfvACbqDUWCqa9mpLLuMmKyOZkGcymJ3NI9LXQfXEDNmn3Wf_GZRbns991rNxmWVn-8u4%3D&query=&page={page}&externalSearch=true&checkedCountries=14360703616&checkedCities='
        
        response = requests.request("POST", url, headers=headers, data=payload)
        data=response.json()["data"]["results"]["jobs"]
        
        for job in data:
            location= "Bucuresti" if job["city"]=="Bucharest" else job["city"]
            title=job["title"]
            # Step 1: Normalize whitespace around hyphens
            title = re.sub(r'\s*-\s*', ' - ', title)
            # Step 2: Standardize use of hyphens
            title = re.sub(r'–', '-', title)  # Replace en-dashes with hyphens
            # Step 3: Remove everything after the last hyphen
            cleaned_title = title.rsplit('-', 1)[0]   
           
            # get jobs items from response
            job_list.append(Item(
                job_title=cleaned_title,
                job_link=job["url"],
                company='Genpact',
                country="România",
                county=location,
                city=location,
                remote=get_job_type(job["title"]),
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Genpact"
    logo_link = "https://mma.prnewswire.com/media/558720/Genpact_Logo.jpg?p=facebook"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
