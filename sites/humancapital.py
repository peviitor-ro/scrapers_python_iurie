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
# Company ---> humancapital
# Link ------> https://recrutaresiselectie.ro/joburi/
#
#
from __utils import (
    GetStaticSoup,
    PostCustumRequest,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from humancapital scraper.
    """
    url = "https://recrutaresiselectie.ro/jm-ajax/get_listings/"

    payload = "lang=ro&search_keywords=&search_location=&search_categories%5B%5D=&filter_job_type%5B%5D=freelance&filter_job_type%5B%5D=full-time&filter_job_type%5B%5D=internship&filter_job_type%5B%5D=part-time&filter_job_type%5B%5D=temporary&filter_job_type%5B%5D=&per_page=200&orderby=featured&featured_first=false&order=DESC&page=1&remote_position=&show_pagination=false&form_data=search_keywords%3D%26search_region%3D0%26search_categories%255B%255D%3D%26filter_job_type%255B%255D%3Dfreelance%26filter_job_type%255B%255D%3Dfull-time%26filter_job_type%255B%255D%3Dinternship%26filter_job_type%255B%255D%3Dpart-time%26filter_job_type%255B%255D%3Dtemporary%26filter_job_type%255B%255D%3D"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'PHPSESSID=1f66ac4c54ea97d81fb946a15c36ee68; cookieyes-consent=consentid:N0FudkZlSW1pWnVrTDdKYXZ2VTJvWlRxTzJNMnk4cEc,consent:,action:,necessary:,functional:,analytics:,performance:,advertisement:',
        'origin': 'https://recrutaresiselectie.ro',
        'priority': 'u=1, i',
        'referer': 'https://recrutaresiselectie.ro/joburi/',
        'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    soup = PostCustumRequest(url=url, headers=headers, payload=payload)
    print(type(soup))
    job_list = []
    for job in soup:  # .find_all("li",class_="job_listings"):
        # print(job)

        # get jobs items from response
        job_list.append(Item(
            job_title="",
            job_link="",
            company="humancapital",
            country="România",
            county="",
            city="",
            remote="",
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "humancapital"
    logo_link = "logo_link"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    # UpdateAPI().publish(jobs)
    # UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
