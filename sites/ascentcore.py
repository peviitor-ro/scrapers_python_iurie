#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> AscentCore
# Link ------> https://api.eu.lever.co/v0/postings/ascentcore?group=team&mode=json
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
    GetRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    """scrape data from AscentCore scraper."""
    json_data = GetRequestJson("https://api.eu.lever.co/v0/postings/ascentcore?group=team&mode=json")

    job_list = []
    for jobs in json_data:
        for job in jobs['postings']:
            # find location from text and location from job['categories']['allLocations']
            if 'Timisoara' in job['descriptionPlain']:
                find_Timisoara = 'Timisoara' 
            # location list
            location=job['categories']['allLocations']
            # add timisoara to list if is on the text but not in the list
            if 'Timisoara' not in location:
                location.append(find_Timisoara)
            #extract county for city
            county = ["Iasi" if city=="Iasi" else get_county_json(city)[0] for city in location]
            
        # get jobs items from response
            job_list.append(Item(
                job_title = job['text'],
                job_link = job['hostedUrl'],
                company = 'AscentCore',
                country = 'România',
                county = county,
                city = location,
                remote = job['workplaceType'],
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AscentCore"
    logo_link = "https://ascentcore.com/wp-content/uploads/2023/08/AC-Logo.svg"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
