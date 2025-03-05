"""
 Basic for scraping data from static pages

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

Company ---> humancapital
Link ------> https://recrutaresiselectie.ro/joburi/
"""

from __utils import (
    GetHtmlSoup,
    PostRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
from datetime import datetime, timedelta


def scraper():
    """
    ... scrape data from humancapital scraper.
    """
    url = "https://recrutaresiselectie.ro/jm-ajax/get_listings/"
    page = 1
    flag = True
    payload = f"lang=ro&search_keywords=&search_location=&search_categories%5B%5D=&filter_job_type%5B%5D=freelance&filter_job_type%5B%5D=full-time&filter_job_type%5B%5D=internship&filter_job_type%5B%5D=part-time&filter_job_type%5B%5D=temporary&filter_job_type%5B%5D=&per_page=100&orderby=featured&featured_first=false&order=DESC&page={page}&remote_position=&show_pagination=false&form_data=search_keywords%3D%26search_region%3D0%26search_categories%255B%255D%3D%26filter_job_type%255B%255D%3Dfreelance%26filter_job_type%255B%255D%3Dfull-time%26filter_job_type%255B%255D%3Dinternship%26filter_job_type%255B%255D%3Dpart-time%26filter_job_type%255B%255D%3Dtemporary%26filter_job_type%255B%255D%3D"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "PHPSESSID=1f66ac4c54ea97d81fb946a15c36ee68; cookieyes-consent=consentid:N0FudkZlSW1pWnVrTDdKYXZ2VTJvWlRxTzJNMnk4cEc,consent:,action:,necessary:,functional:,analytics:,performance:,advertisement:",
        "origin": "https://recrutaresiselectie.ro",
        "priority": "u=1, i",
        "referer": "https://recrutaresiselectie.ro/joburi/",
        "sec-ch-ua": '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    while flag:
        data = PostRequestJson(url=url, custom_headers=headers, data_json=payload)
        job_list = []
        num_of_page = data.get("max_num_pages")
        html_data = data.get("html", "Not Found")
        soup = GetHtmlSoup(html_data)

        for job in soup.find_all("li", class_=lambda x: x and "job_listing" in x):
            # Get class list and check if job is filled
            job_classes = job.get("class", [])

            if (
                "job_position_filled" in job_classes
                or "no_job_listings_found" in job_classes
            ):
                continue

            location = job.find("div", class_="location").text.strip().split(", ")
            title = job.find("h3").text
            county = [get_county_json(city) for city in location]
            # get jobs items from response
            job_list.append(
                Item(
                    job_title=title,
                    job_link=job.find("a")["href"],
                    company="humancapital",
                    country="România",
                    county=county,
                    city="all" if "Remote" in location else location,
                    remote=get_job_type(title),
                ).to_dict()
            )
        if page <= num_of_page:
            page += 1
            payload = f"lang=ro&search_keywords=&search_location=&search_categories%5B%5D=&filter_job_type%5B%5D=freelance&filter_job_type%5B%5D=full-time&filter_job_type%5B%5D=internship&filter_job_type%5B%5D=part-time&filter_job_type%5B%5D=temporary&filter_job_type%5B%5D=&per_page=100&orderby=featured&featured_first=false&order=DESC&page={page}&remote_position=&show_pagination=false&form_data=search_keywords%3D%26search_region%3D0%26search_categories%255B%255D%3D%26filter_job_type%255B%255D%3Dfreelance%26filter_job_type%255B%255D%3Dfull-time%26filter_job_type%255B%255D%3Dinternship%26filter_job_type%255B%255D%3Dpart-time%26filter_job_type%255B%255D%3Dtemporary%26filter_job_type%255B%255D%3D"
        else:
            break

        return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "humancapital"
    logo_link = "https://recrutaresiselectie.ro/wp-content/uploads/2019/04/logo_mare_abc_human.webp"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
