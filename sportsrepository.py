import json
import os
from datetime import date
from model import Score

import requests


class SportsRepository:
    """Repository for getting various sports data."""
    ERROR_MESSAGE = "Please export an environment variable X_RAPIDAPI_KEY."

    def __init__(self):
        api_key = os.getenv('X_RAPIDAPI_KEY')
        if not api_key:
            print(self.ERROR_MESSAGE)
            quit(1)
        self.HEADERS = {
            'x-rapidapi-host': "api-basketball.p.rapidapi.com",
            'x-rapidapi-key': api_key
        }

        current_year = date.today().strftime("%Y")
        next_year = str(int(current_year) + 1)
        self.SEASON = current_year + '-' + next_year

    def get_basketball_score(self, team_id):
        """Gets basketball scores for the current day for a given team ID."""
        query_params = {
            'date': date.today().strftime("%Y-%m-%d"),
            'timezone': 'America/New_York',
            'season': self.SEASON,
            'team': team_id
        }
        url = "https://api-basketball.p.rapidapi.com/games"
        response = requests.get(url, headers=self.HEADERS, params=query_params)
        response_json = json.loads(response.text)

        if response.status_code != 200:
            return Score(errors=response_json['errors'])

        # Only get the first game for now...
        game = response_json['response'][0]

        home_name = game['teams']['home']['name']
        away_name = game['teams']['away']['name']
        home_score = game['scores']['home']['total']
        away_score = game['scores']['away']['total']

        return Score(home_name, away_name, home_score, away_score)
