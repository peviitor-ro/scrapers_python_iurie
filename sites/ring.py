#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Ring
# Link ------> https://www.amazon.jobs/api/jobs/search
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
    ... scrape data from Ring scraper.
    '''
    payload = "{\"accessLevel\":\"EXTERNAL\",\"contentFilterFacets\":[{\"name\":\"primarySearchLabel\",\"requestedFacetCount\":9999,\"values\":[{\"name\":\"alexa-and-amazon-devices.team-ring-key-blink\"}]}],\"excludeFacets\":[{\"name\":\"isConfidential\",\"values\":[{\"name\":\"1\"}]},{\"name\":\"businessCategory\",\"values\":[{\"name\":\"a-confidential-job\"}]}],\"filterFacets\":[],\"includeFacets\":[],\"jobTypeFacets\":[],\"locationFacets\":[[{\"name\":\"country\",\"requestedFacetCount\":9999,\"values\":[{\"name\":\"RO\"}]},{\"name\":\"normalizedStateName\",\"requestedFacetCount\":9999},{\"name\":\"normalizedCityName\",\"requestedFacetCount\":9999}]],\"query\":\"\",\"size\":10,\"start\":0,\"treatment\":\"OM\",\"cookieInfo\":\"\",\"sort\":{\"sortOrder\":\"DESCENDING\",\"sortType\":\"SCORE\"}}"
    headers = {
    'accept': 'application/json',
    'x-api-key': 'PbxxNwIlTi4FP5oijKdtk3IrBF5CLd4R4oPHsKNh',
    'Content-Type': 'text/plain',
    'Cookie': '__Host-mons-sid=260-7022421-7584047; __Host-mons-st=+bMolpSJw7PqZOxGJVriXhh/ase84s9QoKAUSnEEubTmy/H77//EXVU6b5LqrVJ3u84D1fLGkqTKTUasffN5AhjqbiyaymiR0CQD/F5k1c3oVHUwAh2QT5jZBEEAaeUm9nRInALg2u51lzOfnA+qFJM0suStGD/oUW7sWs6OjdYsQI3p4lLBG6xzIoWun/CXDndI15bVoXL77rVBGhKIbpJRXh9xQ6I7yQ2C1Ass1PMvkN4c1ZJ3ME9uzfPsfw9TXlAF8c9YioZi268aWkPrW/aixIf3ThsiWwm+jHK1UcHlOFkzA+P/yUNldlFqhLHlLPYcMO1QQKuneuag8TfCAzuqqypNPPpWdPpQiNMZEns=; __Host-mons-ubid=257-3119410-4429648'
    }
    post_data = PostRequestJson("https://www.amazon.jobs/api/jobs/search", custom_headers=headers, data_raw=payload)
    
    job_list = []
    for job in post_data["searchHits"]:
        location = job["fields"]["normalizedCityName"][0]
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job["fields"]["title"][0],
            job_link="https://www.amazon.jobs/en/jobs/"+job["fields"]["icimsJobId"][0],
            company='Ring',
            country="România",
            county="Iasi" if "Iasi" in location else get_county_json(location),
            city=job["fields"]["normalizedCityName"][0],
            remote=get_job_type(job["fields"]["locations"][0]),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Ring"
    logo_link = "https://download.logo.wine/logo/Ring_Inc./Ring_Inc.-Logo.wine.png"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
