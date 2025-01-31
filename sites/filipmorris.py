"""
Config for Dynamic Get Method -> For Json format!

Company ---> filipmoris
Link ------> https://join.pmicareers.com/gb/en/search-results?p=ChIJw3aJlSb_sUARlLEEqJJP74Q&location=Romania

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)
"""
import subprocess
import re
import json

from __utils import (
    GetRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    '''
    ... scrape data from filip moris scraper.
    '''
    # URL to fetch data from
    url = "https://join.pmicareers.com/gb/en/search-results?keywords=&p=ChIJw3aJlSb_sUARlLEEqJJP74Q&location=Romania"

    # Use curl to fetch the page content
    curl_command = ["curl", "-s", "-A", "Mozilla/5.0", url]
    html_output = subprocess.run(curl_command, capture_output=True, text=True).stdout

    # Use regex to extract only JSON till "jobwidgetsettings"
    match = re.search(r'"eagerLoadRefineSearch":\s*({.*?})\}]', html_output, re.DOTALL)


    if match:
        # Extract only the "jobs" array
        jobs_data = match.group(1)
        print (jobs_data)
        try:
            jobs_list = json.loads(jobs_data)  # Convert the jobs data to Python list

            # Pretty print the jobs array
            print(json.dumps(jobs_list, indent=4))

        except json.JSONDecodeError as e:
            print(f"❌ JSON decoding error: {e}")
    else:
        print("❌ Jobs data not found in HTML.")

    job_list = []
    for job in jobs_list:
        print(job)

        # get jobs items from response
        job_list.append(Item(
            job_title="",
            job_link="",
            company="filipmoris",
            country="România",
            county="",
            city="",
            remote="",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "filipmoris"
    logo_link = "logo_link"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    #UpdateAPI().publish(jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
