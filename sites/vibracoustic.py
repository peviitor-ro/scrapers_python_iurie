#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Vibracoustic
# Link ------> https://jobs.freudenberg.com/Freudenberg/api/json/?company=VC&location=L_00000250
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
import json
import subprocess

from __utils import Item, UpdateAPI


API_URL = "https://r.jina.ai/https://jobs.freudenberg.com/Freudenberg/api/json/?company=VC&location=L_00000250"


def _load_jobs():
    for attempt in range(3):
        try:
            result = subprocess.run(
                [
                    "curl", "-s", "--max-time", "30",
                    "-A", "Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8 like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.14",
                    "-H", "X-Return-Format: markdown",
                    API_URL,
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False,
            )
            if result.returncode == 0:
                text = result.stdout.decode("utf-8")
                start = text.find("{")
                end = text.rfind("}")
                if start != -1 and end != -1 and end > start:
                    return json.loads(text[start:end + 1])
        except Exception:
            pass
    return {"jobs": []}

def scraper():
    '''
    ... scrape data from Vibracoustic scraper.
    '''
    # https://jobs.freudenberg.com/Freudenberg/?company=VC&location=RO
    json_data = _load_jobs()

    job_list = []
    for job in json_data['jobs']:

        # get jobs items from response
        job_list.append(Item(
            job_title=job["jobtitle"],
            job_link=job["deepLink"],
            company="Vibracoustic",
            country="România",
            county="Dej",
            city="Dej",
            remote="Hybrid",
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Vibracoustic"
    logo_link = "https://www2.solique.ch/templateimages/Freudenberg/img/logos/Vibracoustic.svg"

    jobs = scraper()
    print("jobs found:",len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
