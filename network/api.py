import json

import requests


class Api:
    """Client for communicating with various APIs"""
    BASE_URL = 'https://api-basketball.p.rapidapi.com'

    def __init__(self, api_key: str):
        self.HEADERS = {
            'x-rapidapi-host': "api-basketball.p.rapidapi.com",
            'x-rapidapi-key': api_key
        }

    def get(self, path: str, params: object):
        """Performs a get request on the given path with the given parameters."""
        url = self.BASE_URL + path
        response = requests.get(url, headers=self.HEADERS, params=params)

        if response.status_code != 200:
            raise Exception("Failed with status code %d" % response.status_code)

        return json.loads(response.text)