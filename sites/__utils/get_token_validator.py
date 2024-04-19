import requests
import os
import json
# from dotenv import load_dotenv

# load_dotenv()

domain = os.environ.get("DOMAIN")


def get_token():
    """
    Returnează token-ul necesar pentru a face request-uri către API.
    :return: token-ul necesar pentru a face request-uri către API
    """
    endpoint = os.environ.get("TOKEN_ROUTE")
    email = os.environ.get("EMAIL")
    url = f"{domain}{endpoint}"
    response = requests.post(url, json={"email": email})
    return response.json()["access"]

print(get_token())