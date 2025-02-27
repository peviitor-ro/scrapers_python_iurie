"""

Config for Dynamic Post Method -> For Json format!

Company ---> Gopro
Link ------> https://jobs.gopro.com/api/v1/jobs/external

------ IMPORTANT! ------
if you need return soup object:
you cand import from __utils -> GetHtmlSoup
if you need return regex object:
you cand import from __utils ->
---> get_data_with_regex(expression: str, object: str)

"""

from __utils import (
    PostRequestJson,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from Gopro scraper.
        https://jobs.gopro.com/en/pl
    """
    url = "https://jobs.gopro.com/api/appSearch"

    payload = '{"query":"","search_fields":{"title":{},"location":{},"category":{},"city_filter":{},"country_filter":{}},"result_fields":{"title":{"raw":{}},"location":{"raw":{}},"job_type":{"raw":{}},"content":{"snippet":{"fallback":true}},"category":{"raw":{}},"country_filter":{"raw":{}},"city_filter":{"raw":{}},"url":{"raw":{}}},"precision":2,"page":{"size":5,"current":1},"filters":{"all":[{"any":[{"location":"Bucharest"}]},{"any":[{"group_id":2082}]},{"any":[{"live":1}]}]},"facets":{"category":{"type":"value","size":30},"location":{"type":"value","size":30},"job_type":{"type":"value","size":30}}}'
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-xsrf-token": "eyJpdiI6ImFoS05FUmtDV1R1cnI2d1NZZjFSWmc9PSIsInZhbHVlIjoieVFWMXZJQ0krL25zN0VPMzB0MjVQRi9INFdFMWpQQStLcCtEVjB1TmNvK2YwWkRab3UxT2t3Y0JDSFVrVklEcVVkOVJ5ZHJtYlZxR1pFUjd5NFhpZDhFQWMzZDRUYyt6LzRSelZneURFdldrUzZOS1hVUkxldmh3VnI3dTk2MEkiLCJtYWMiOiJiMmU1YzNjMjAwZTFjMjAzNjAxYTU0ZGVmMzE4MGI5NWQyN2E4NjMyNGRhZjg1YjAyMmM5ZWQ4ZGYxMTk2ZWFjIiwidGFnIjoiIn0=",
        "Cookie": "XSRF-TOKEN=eyJpdiI6ImxPUnJQUXNYNDllWEpXMTNTdlp6cnc9PSIsInZhbHVlIjoiNFhPcXdvSW5BVjhJd1ZaQmRKOSs0Q2pqSElqSUpRQXZkNUhTMlR4amU5dE1ZOHl6ME8xNEZENjlCZ2JNSGZMK2p0M2ZUR2E5b2RUenRoU1ltVkJQTTFPUk1BM3EyRVVhVStQbmpPdVBQVktjS1hwaGdESk9xMjJNUWgzVHpMaHEiLCJtYWMiOiIyMGNjY2JkY2E5ZWJmMDU1MWMxYzZlNDI4ODlmYjhjMTcyMmQ4YjAwMWIwYTE0YTAwOWFjY2Q4ZDYzOGI1MjAxIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IkVzaS9FWGtaU25KemV2WUtMYzQ1YlE9PSIsInZhbHVlIjoiL0VEWDlBT2tJRlJmZU1GU2FMS1JCTVc3R3V0RzczVjIrZEd4Zi9DZWljM3R4RDFxTXlYNnZ6Y1dCTjBnNEk2a0hQNzBkLzlwclVsdVRHckhtTUxVZ1pQTk5mMDhJOVRhYTJSVm8vajJER25rRS9zeE1raUowYS9VMW9wNFJ6cEQiLCJtYWMiOiI3MThmZGRlODdhOTQwZDI4MjIzMjM2NThlMTAzMjY0MTk3OWZkYzAyMDBhNTY3N2NhNzM0ODg4OGJhNmI1Y2ZkIiwidGFnIjoiIn0%3D",
    }

    post_data = PostRequestJson(url=url, custom_headers=headers, data_raw=payload)

    job_list = []

    for job in post_data["results"]:
        city = (
            "Bucuresti"
            if "bucharest" in job["city_filter"]["raw"]
            else job["city_filter"]["raw"]
        )
        job_type = job["job_type"]["raw"].lower()

        # get jobs items from response
        job_list.append(
            Item(
                job_title=job["title"]["raw"],
                job_link="https://jobs.gopro.com/en/us/jobs/" + job["url"]["raw"],
                company="Gopro",
                country="România",
                county="all" if "remote" in job_type else get_county_json(city),
                city="all" if "remote" in job_type else city,
                remote=job_type,
            ).to_dict()
        )

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "Gopro"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/c/c3/GoPro_logo.svg"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
