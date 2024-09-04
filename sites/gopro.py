#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Gopro
# Link ------> https://jobs.gopro.com/api/v1/jobs/external
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
    ... scrape data from Gopro scraper.
        https://jobs.gopro.com/jobs/country/romania#/
    '''
    payload = {
        "group": "gopro",
        "group_id": "1613",
        "filters": "{}",
        "query": "romania",
        "from": 0,
        "mobile": 0,
        "session": "",
        "old_search": 0
    }
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'AWSALB=m5XxeCbKRY1b4KD/PkmrEgEd2oPkqQJ38hHCR8uPvM7b0HcFZJoEz3+UZsy3SeugUixwNtVoYAX/orDD0biR5+rO9ZjgdP2YvKpg+hnEhZDPRAk8ENEKuXe3HhVI; AWSALBCORS=m5XxeCbKRY1b4KD/PkmrEgEd2oPkqQJ38hHCR8uPvM7b0HcFZJoEz3+UZsy3SeugUixwNtVoYAX/orDD0biR5+rO9ZjgdP2YvKpg+hnEhZDPRAk8ENEKuXe3HhVI; XSRF-TOKEN=eyJpdiI6InlmdEVKdG5uK3l1NU9UMU5wQ1BSc1E9PSIsInZhbHVlIjoiR1Q4c0YzeitraHBFNGh3cFhwVHluNVp5SnI4WlFJdERTYUZQMFJObHhkQjBEWXpzZTFQanZoNnErY25EcjM1aENMbWZ5VHJYZjdRZll2bVREUEUvamMwWUNPMFZ4NytQT3dJZ1ZISWpsOFRYeXUvN085Q1hQYmRLNWxjSEJKcVkiLCJtYWMiOiI2ZDhmNTVmMGU4NjYzNzVlNzU4YThmZGVhZDM4MTc1NzA1ZmRmOGRiZjZhMTAwMDI0YWRmM2VjM2QzOTRiYTNmIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6ImgzRWFLeDBMVVY4Y3FVNUZrTXZvYUE9PSIsInZhbHVlIjoieHlsdkxCT1F2UjBzZWtQakJmaHRoY1VBVE82cnhlcnJCVnNpckFGVThQT0cyVGVZUWVEdUFmcFkzdVJSQXc3aEdWdklnWjc0cWZxSVVxT08rRW5rL1pJVnVZclBPVVcrT2NQQmM1cGxOUlljd3lDelBLemRuN2ZzamRIeHBoaXoiLCJtYWMiOiIyYzRiZWE3NGQwNDg5ZTcyNTQ3M2M2MTg2MzE4MGRhZTAyYjkzYTg0NmQ2YjgzMzJhY2JmZDBmNTFiNzU1ODA2IiwidGFnIjoiIn0%3D'
    }
    post_data = PostRequestJson(
        "https://jobs.gopro.com/api/v1/jobs/external", custom_headers=headers, data_json=payload)

    job_list = []
    for job in post_data["response"]["matchingJobs"]:
        location = get_job_type(job["jobSummary"])

        # get jobs items from response
        job_list.append(Item(
            job_title=job["jobTitleSnippet"],
            job_link=job["job"]["customAttributes"]["url"]["stringValues"][0],
            company='Gopro',
            country="România",
            county="all" if "remote" in location else location,
            city="all" if "remote" in location else location,
            remote=get_job_type(job["jobSummary"]),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Gopro"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/c/c3/GoPro_logo.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
