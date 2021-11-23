from datetime import date

from network.api import Api
from model import Game, GameStatus


class GameRepository:
    """Repository for getting score data."""
    ERROR_MESSAGE = "Please export an environment variable X_RAPIDAPI_KEY."

    def __init__(self, api_client: Api):
        self.api_client = api_client
        current_year = date.today().strftime("%Y")
        next_year = str(int(current_year) + 1)
        self.SEASON = current_year + '-' + next_year

    def get_basketball_score(self, team_id) -> Game:
        """Gets basketball scores for the current day for a given team ID."""
        query_params = {
            'date': date.today().strftime("%Y-%m-%d"),
            'timezone': 'America/New_York',
            'season': self.SEASON,
            'team': team_id
        }

        response_json = self.api_client.get('/games', query_params)

        games = response_json['response']
        if not games:
            return Game(game_status=GameStatus.NO_GAME)

        game = response_json['response'][0]

        home_name = game['teams']['home']['name']
        away_name = game['teams']['away']['name']
        home_score = game['scores']['home']['total']
        away_score = game['scores']['away']['total']

        status = self.__status_from_response(game)
        if status == GameStatus.NOT_STARTED:
            game_time = game['time']
        else:
            game_time = game['status']['long']

        return Game(status, home_name, away_name, home_score, away_score, game_time=game_time)

    def __status_from_response(self, game) -> GameStatus:
        # TODO(dpowers): implement case for final
        status = game['status']['short']
        if status == 'NS':
            return GameStatus.NOT_STARTED
        return GameStatus.IN_PROGRESS
