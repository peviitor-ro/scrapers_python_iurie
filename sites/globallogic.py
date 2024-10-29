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
# Company ---> globallogic
# Link ------> https://www.globallogic.com/career-search-page/page/1/?keywords&experience&locations=romania&c
#
#
from __utils import (
    GetStaticSoup,
    RequestsCustum,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)
from bs4 import BeautifulSoup


def scraper():
    """
    ... scrape data from globallogic scraper.
    """
    page = 1
    url = f"https://www.globallogic.com/career-search-page/page/1/?keywords&experience&locations=romania&c"

    payload = {}
    headers = {
        'Cookie': 'incap_ses_324_1279438=qRoLJ4SgbzegytCEVhR/BNKpIGcAAAAAVaTYjgljkvDdmpdyLc1wGw==; visid_incap_1279438=Ps0QFb7pRrW4mEDxOB/F+7+pIGcAAAAAQUIPAAAAAAAzzcXj1EATKZ9nhSZEWJp6; PHPSESSID=68hmh3g23aeflo3etkoov639l4; locations=romania; wordpress_google_apps_login=789a878c2075bd7d640fdc9992f86955'
    }
    response = RequestsCustum(url=url, payload=payload, headers=headers)
    # convert response to  html  object
    soup = BeautifulSoup(response, "lxml")

    job_list = []
    # find  number of pages
    pages = soup.find("span", class_="pages").text.split()[-1]

    for page in range(2, int(pages)+2):

        for job in soup.find_all("div", class_="career-pagelink"):
            job_type = job.find("span",  class_="remote-badge").text
            location = job.find("span", class_="job-locations").text

            # Check if a specific city is listed after "Romania -"
            if "Romania -" in location:
                # Extract city names after "Romania -"
                city_part = location.split("Romania -", 1)[1].strip()
                city_list = ["Bucuresti" if "Bucharest" in city.strip(
                ) else city.strip() for city in city_part.split(',')]
                cities = city_list
            else:
                # If no specific city, add "all"
                cities = ["all"]

            # Find county for city
            county = ["all" if "all" == city else "Iasi" if "Iasi" ==
                      city else get_county_json(city)[0] for city in cities]

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find("p",  class_="mb-0").text,
                job_link=job.find("p",  class_="mb-0").find("a")["href"],
                company="globallogic",
                country="România",
                county=county,
                city=cities,
                remote=get_job_type(job_type),
            ).to_dict())
        # incriment pages and make next request
        url = f"https://www.globallogic.com/career-search-page/page/{page}/?keywords&experience&locations=romania&c"
        response = RequestsCustum(url=url, payload=payload, headers=headers)
        soup = BeautifulSoup(response, "lxml")
    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "globallogic"
    logo_link = "https://www.globallogic.com/wp-content/uploads/2021/11/Wordmark.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
