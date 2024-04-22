#
#
#
#  Send data to Peviitor API!
#  ... OOP version
#
#
import requests
#
import json


class UpdateAPI:
    '''
    - Method for update data,
    - Method for update logo.
    '''

    def __init__(self):
        self.logo_url = 'https://api.peviitor.ro/v1/logo/add/'   
        self.logo_header = { 'Content-Type': 'application/json'}
        
        self.EMAIL = 'chigaiiura@yahoo.com'
        self.DOMAIN = 'https://api.peviitor.ro/v5/'

        self.TOKEN_ROUTE = 'get_token/'
        self.ADD_JOBS_ROUTE = 'add/'


    def update_logo(self, id_company: str, logo_link: str):
        '''update logo on peviitor.ro'''

        data = json.dumps([{"id": id_company, "logo": logo_link}])
        response = requests.post(self.logo_url, headers=self.logo_header, data=data)

        #  print(f'Logo update ---> succesfuly {response}')
        
    def get_token(self):
        """
        Returnează token-ul necesar pentru a face request-uri către API.
        :return: token-ul necesar pentru a face request-uri către API
        """
        endpoint = self.TOKEN_ROUTE
        email = self.EMAIL
        url = f"{self.DOMAIN}{endpoint}"
        response = requests.post(url, json={"email": email})
        return response.json()["access"]

    def publish(self, data):
        """This method publish scraped data using API to Validator with post method
        using token to make API request.
        Args:
            data (_type_): Json
        """
        
        route = self.ADD_JOBS_ROUTE
        url = f"{self.DOMAIN}{route}"
        token = self.get_token()

        headers = {"Content-Type": "application/json",
                "Authorization": f"Bearer {token}"}

        requests.post(url, headers=headers, json=data)
       
        print(json.dumps(data, indent=4))
        
    