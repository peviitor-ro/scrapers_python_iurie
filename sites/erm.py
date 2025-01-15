#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> ERM
# Link ------> https://erm.wd3.myworkdayjobs.com/wday/cxs/erm/ERM_Careers/jobs
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
    ... scrape data from ERM scraper.
    '''
    payload = {
        "appliedFacets": {
            "locations": [
                "94e33b804cf847a8a4e09b0bf8d508c6"
            ]},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US',
        'content-type': 'application/json',
        'cookie': 'wday_vps_cookie=3109591306.53810.0000; timezoneOffset=-120; PLAY_SESSION=7b8ab2c2a7ce7d14efd8af1257d4d42b86732224-erm_pSessionId=r1977i2f0ql02c3v4fqo9dc073&instance=vps-prod-1g11zjbf.prod-vps.pr501.cust.dub.wd; __cf_bm=poOtt3wr6kVC3bAupO5DlOJuDtS.c0iISscGnzO_6bw-1718187117-1.0.1.1-gFDn7waW6xgKrLcSvezJ7NYGmz3kJRPHYj4TVgirALjf13CvmSzMIXFA3YISvn5TjpWC1FkZ1xjmfZb9K3jHlQ; __cflb=02DiuJFb1a2FCfph91kR4XMuWBo9zS6ftkDcYLNqJrM8g; _cfuvid=.iVaGLZW70U5cOmi5vHdWRgHGjMV_GXEyVE2u3iX6Rk-1718187117880-0.0.1.1-604800000; wd-browser-id=b63e336e-304d-46f1-bcc3-dc47530fa0a5; CALYPSO_CSRF_TOKEN=5aadf75a-9a61-4770-a1f9-3c9cecd088b0; PLAY_SESSION=7b8ab2c2a7ce7d14efd8af1257d4d42b86732224-erm_pSessionId=r1977i2f0ql02c3v4fqo9dc073&instance=vps-prod-1g11zjbf.prod-vps.pr501.cust.dub.wd; __cf_bm=BPWUwJ.L__15rHmU9.d4Ypd3.mO.ZUWGVmrHkTbLt3I-1718187217-1.0.1.1-OeYht2x2Q.yrUqytKXo5_G92uQiS3S5bfXY7JouPceTu9T1UrQ.BL7q5aJACLUgISC5Ds9sytFxwZq3JKDhRVA; __cflb=02DiuJFb1a2FCfph91mEfCE19uWmaV9PDsS5GS1zHXP5v; _cfuvid=.0peGwG3L4Pkm74Aq2Fu8b_uVa6qc8PaVKS40qIFNzA-1718187217125-0.0.1.1-604800000; wd-browser-id=a2bcc3ee-b857-4531-b1d2-e01a679ba63d; wday_vps_cookie=3109591306.53810.0000',
        'origin': 'https://erm.wd3.myworkdayjobs.com',
        'priority': 'u=1, i',
        'referer': 'https://erm.wd3.myworkdayjobs.com/ERM_Careers?locations=94e33b804cf847a8a4e09b0bf8d508c6',
        'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-calypso-csrf-token': '5aadf75a-9a61-4770-a1f9-3c9cecd088b0'
    }
    post_data = PostRequestJson(
        "https://erm.wd3.myworkdayjobs.com/wday/cxs/erm/ERM_Careers/jobs", custom_headers=headers, data_json=payload)

    job_list = []
    for job in post_data["jobPostings"]:
        location = "București"if "Bucharest" in job["locationsText"] else job["locationsText"]

        # get jobs items from response
        job_list.append(Item(
            job_title=job["title"],
            job_link="https://erm.wd3.myworkdayjobs.com/en-US/ERM_Careers" +
            job["externalPath"],
            company='ERM',
            country="România",
            county=get_county_json(location),
            city="București" if job["title"] == "Principal REACH Consultant (m/w/d)" else location,
            remote="on-site" if job["title"] == "Principal REACH Consultant (m/w/d)" else "remote",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ERM"
    logo_link = "https://erm.wd3.myworkdayjobs.com/wday/cxs/erm/ERM_Careers/sidebarimage/44b6c2a958561000fe7b755b502d0000"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
