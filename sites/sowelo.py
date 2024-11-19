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
# Company ---> Sowelo
# Link ------> https://soweloconsulting.applytojob.com/apply/jobs?&
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
    ... scrape data from Sowelo scraper.
    """
    soup = GetStaticSoup("https://soweloconsulting.applytojob.com/apply/jobs?&")

    job_list = []
    class_row=["resumator_even_row", "resumator_odd_row"]
    for row_class in class_row:
        for job in soup.find_all("tr",attrs=row_class):
            td_elements = job.find_all('td')
            # Check if "Romania" is in the text of the second <td>
            if "Romania" in td_elements[1].get_text():
                # Print the text of the <a> tag in the first <td>
                title=job.find('a', attrs="job_title_link").text
                link = "https://soweloconsulting.applytojob.com"+job.find("a", attrs="job_title_link").get("href")
                
                # get jobs items from response
                job_list.append(Item(
                    job_title=title,
                    job_link=link,
                    company="Sowelo",
                    country="România",
                    county="București", 
                    city="București",
                    remote=get_job_type(title),
                ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Sowelo"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvjHLNHWH9V7VQ3qOP8EP-xqnvwSICQsjlsX7vfFswjQ&s"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
