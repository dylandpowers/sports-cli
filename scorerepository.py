from datetime import date

from network.api import Api
from model import Score


class ScoreRepository:
    """Repository for getting score data."""
    ERROR_MESSAGE = "Please export an environment variable X_RAPIDAPI_KEY."

    def __init__(self, api_client: Api):
        self.api_client = api_client
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

        response_json = self.api_client.get('/games', query_params)
        # Only get the first game for now...
        game = response_json['response'][0]

        home_name = game['teams']['home']['name']
        away_name = game['teams']['away']['name']
        home_score = game['scores']['home']['total']
        away_score = game['scores']['away']['total']

        return Score(home_name, away_name, home_score, away_score)
