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
# Company ---> MORGANSOL
# Link ------> https://www.morgansol.ro/page/2/?post_type=job_listing
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from MORGANSOL scraper.
    """
    job_list = []
    #check how many pages with jobs are on the page 
    # soup = GetStaticSoup("https://www.morgansol.ro/?post_type=job_listing")
    # pages=int(soup.find_all("a", class_="page-numbers")[-2].text.split()[-1])
    for page in range(1,2):
        soup=GetStaticSoup(f"https://www.morgansol.ro/page/{page}/?post_type=job_listing")
        for job in soup.find_all("div",attrs="blog-entry-inner entry-inner wpex-last-mb-0 wpex-clr"):
            link=job.find("h2", class_="blog-entry-title entry-title wpex-text-3xl").find("a")["href"]
            job_detail=GetStaticSoup(link)
            job_detail.find("div", class_="single_job_listing")
            if len(job_detail.contents)>1:
                location=job_detail.find("li", class_="location")
                if location:
                    city=location.text.split(",")[0].capitalize()
                    
                    # get jobs items from response
                    job_list.append(Item(
                        job_title=job.find("h2", class_="blog-entry-title entry-title wpex-text-3xl").text,
                        job_link=link,
                        company="MORGANSOL",
                        country="România",
                        county=get_county_json(city),
                        city=city,
                        remote=get_job_type(job_detail.find("div", class_="job_description").text),
                    ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "MORGANSOL"
    logo_link = "https://www.morgansol.ro/wp-content/uploads/2023/05/LOGO-MORGANSOL.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
