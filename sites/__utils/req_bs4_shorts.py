#
#
#  This file contains the Requests + BS4 shorts;
#  Avoid DRY code, its not a good practice!!!
#  Make Python3 better place for code!
#
#  Start here!
#
# Note ---> Update certifi for bad SSL
# if SSL invalid ---> rezolve without error in terminal
# ... plus sa fac aceeasi chestie ca la PostRequestJson si in GetRequestJson
#
import requests
from bs4 import BeautifulSoup
#
import cfscrape
#
from .default_headers import DEFAULT_HEADERS
#
import xml.etree.ElementTree as ET

import subprocess


# Global Session -> avoid multiple requests
# ... and all classes can use it in one script
session = requests.Session()


class GetCustumRequest:
    """scrape data with requests

    Returns:
        _type_: responce.text
    """
    def __new__(cls, url, headers, payload):
        try:
            response = session.request(
                "GET", url, headers=headers, data=payload)
            return BeautifulSoup(response.text, 'lxml')
        except ValueError:
            raise Exception("Request error", session)
        finally:
            response.close()


class PostCustumRequest:
    """scrape data with requests Post

    Returns:
        _type_: responce.text
    """
    def __new__(cls, url, headers, payload):

        try:
            response = session.request(
                "POST", url, headers=headers, data=payload)
            return BeautifulSoup(response.text, 'lxml')
        except ValueError:
            raise Exception("Request error", session)
        finally:
            response.close()


class GetStaticSoup:
    '''
    ... This class return soup object from static page!
    '''

    def __new__(cls, url, custom_headers=None):

        headers = DEFAULT_HEADERS.copy()

        #  if user have custom headers,
        #  update the headers
        if custom_headers:
            headers.update(custom_headers)
        try:
            response = session.get(url, headers=headers)
            # return soup object from static page
            return BeautifulSoup(response.text, 'lxml')
        except ValueError:
            raise Exception("soup request", response.status_code)
        finally:
            response.close()


class GetRequestJson:
    '''
    ... This class return JSON object from get requests!
    '''

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # Dacă utilizatorul are headere personalizate, actualizează headerele
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(url, headers=headers)

        # Parse response to JSON and return ditct oject
        try:
            json_response = response.json()
            return json_response
        except ValueError:
            return BeautifulSoup(response.text, 'lxml')
        finally:
            response.close()


class PostRequestJson:
    '''
    ... This class return JSON object from post requests!
    '''

    def __new__(cls, url, custom_headers=None, data_raw=None, data_json=None):
        headers = DEFAULT_HEADERS.copy()

        # Post requests headers, if not provided
        if custom_headers:
            headers.update(custom_headers)

        if data_json:
            response = session.post(url, headers=headers, json=data_json)
        else:
            response = session.post(url, headers=headers, data=data_raw)

        try:
            return response.json()
        except ValueError:
            return BeautifulSoup(response.text, 'lxml')
        finally:
            response.close()


class GetHtmlSoup:
    '''
    ... method if server return html response,
    after post requests.
    '''

    def __new__(cls, html_response):
        return BeautifulSoup(html_response, 'lxml')


class GetHeadersDict:
    '''
    ... method if server return headers response,
    after session.headers
    '''

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # Post requests headers, if not provided
        if custom_headers:
            headers.update(custom_headers)

        response = session.head(url, headers=headers).headers

        return response


class HackCloudFlare:
    '''
    ... this method can help you avoid CloudFlare protection.
    Is not a hack, but useful tool.
    '''

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # if headers is requiered
        if custom_headers:
            headers.update(custom_headers)

        scraper = cfscrape.create_scraper()

        return BeautifulSoup(scraper.get(url).content, 'lxml')


class GetXMLObject:
    '''
    ... this class will return data from XML stored in a list
    '''

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # if custom headers
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return ET.fromstring(response.text)


class GetDataCurl:

    def __new__(cls, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        }

        try:
            # Construct the curl command
            command = [
                'curl', '-s', '-A', headers['User-Agent'], url
            ]
            # Execute the curl command and capture the output
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False)
            # Check if there was an error
            if result.returncode != 0:
                raise Exception(result.stderr.decode('utf-8'))
            # Decode the output using utf-8
            data = result.stdout.decode('utf-8')
            # convert decoded data to text
            soup = BeautifulSoup(data, "lxml")
            return soup.get_text()
        except Exception as e:
            # Handle exceptions (e.g., network errors, invalid responses)
            print(f"An error occurred: {e}")
            return None
