import requests
from __utils.peviitor_update import UpdateAPI

"""this code is checking all scraper file and if new scraper is created it adding it 
    in Dockker validator
"""

url = "https://api.laurentiumarian.ro/scraper/scrapers_python_iurie/"

token = UpdateAPI().get_token()

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

r = requests.post(url, json={"update": "true"}, headers=headers)

response = r.json()

if response.get("success"):
    print(response.get("success"))
else:
    print(response.get("error"))
