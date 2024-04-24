import requests
from sites.__utils.peviitor_update import UpdateAPI

EMAIL = 'chigaiiura@yahoo.com'
DOMAIN = 'https://api.peviitor.ro/v5/'

TOKEN_ROUTE = 'get_token/'
endpoint = TOKEN_ROUTE
url = f"{DOMAIN}{endpoint}"

token = UpdateAPI.get_token()

print(token)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

response = requests.post(url, json = {"update": "true"}, headers=headers)

print(response.status_code)

