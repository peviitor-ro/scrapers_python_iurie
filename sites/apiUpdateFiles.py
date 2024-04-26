import requests 
from __utils.peviitor_update import UpdateAPI

url = "https://api.laurentiumarian.ro/scraper/scrapers_python_iurie/" 
 

token = UpdateAPI().get_token()

# print(token)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

response = requests.post(url, json = {"update": "true"}, headers=headers)

print(response.status_code)

