#
# ... new file for Clean_data from API
#

import os
import requests
import subprocess

class CleanData:

    def __init__(self):
        # Run source enviroment.sh
        path="/Users/Scraping/scrapers_python_iurie/enviroment.sh"
        comand=f"source {path}"
        subprocess.run(["bash","-c", comand],capture_output=True,)
        self.api_key = os.environ.get("API_KEY_PEVIITOR")
        self.clean_url = "https://api.peviitor.ro/v4/clean/"

    def clean_data(self, company_name: str) -> None:
        clean_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "apikey": self.api_key
        }

        clean_request = requests.post(url=self.clean_url, headers=clean_header,
                                      data={"company": company_name})
        print(f"{company_name} clean all Data -> {clean_request.status_code}")


class ConcreteCleanData(CleanData):

    def __fspath__(self):
        return self.clean_url


def main():

    # company name, from terminal
    input_company = input("Scrie numele companiei: ")

    # create a ConcreteCleanData object
    # clean_data = ConcreteCleanData(api_key=os.environ.get("API_KEY"))

    # clean data
    # clean_data.clean_data(input_company)


if __name__ == "__main__":
    CleanData().clean_data('Computacenter')
    # main()
