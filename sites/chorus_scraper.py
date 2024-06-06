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
# Company ---> Chorus
# Link ------> https://www.chorus.ro/job_list
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
    ... scrape data from Chorus scraper.
    """
    soup = GetStaticSoup("https://www.chorus.ro/job_list")

    job_list = []
    for job in soup.find_all('ul', attrs=('descr')):
        for data in job.find_all('li'):
            #extract location from page 
            br_tag = data.find('br') #find <br> and assigne it to variable
            if br_tag:
                #create a list of locations
                locations = br_tag.next_sibling.strip().split(', ') 
                
                #replace incorect location from a list
                if 'MogosoaiaSe' in locations[0]:
                    locations[0] = 'Mogosoaia'
                    locations.append('Bucuresti')
                
                #extract county for locations 
                check_county=[get_county_json(county) for county in locations ]
                clean_county=[item for sublist in check_county for item in sublist]
                unic_county=list(set(clean_county))
            
                # get jobs items from response
                job_list.append(Item(
                    job_title = data.find('a').text.strip(),
                    job_link = data.find('a')['href'],
                    company = 'Chorus',
                    country = 'România',
                    county = unic_county,
                    city = locations,
                    remote = 'on-site',
                ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Chorus"
    logo_link = "https://www.chorus.ro/images/design/logo.png"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
