from datetime import date
import tzlocal

from network.api import Api
from model import Game, GameStatus


class GameRepository:
    """Repository for getting score data."""
    ERROR_MESSAGE = "Please export an environment variable X_RAPIDAPI_KEY."

    def __init__(self, api_client: Api):
        self.api_client = api_client

    def get_basketball_score(self, team_id: int) -> Game:
        """Gets basketball scores for the current day for a given team ID."""
        query_params = {
            'date': date.today().strftime("%Y-%m-%d"),
            'timezone': tzlocal.get_localzone_name(),
            'season': '2021-2022',  # TODO(dpowers) dynamically generate this
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
        elif status == GameStatus.IN_PROGRESS:
            game_time = game['status']['long']
        else:
            game_time = 'Final'

        return Game(status, home_name, away_name, home_score, away_score, game_time=game_time)

    def __status_from_response(self, game) -> GameStatus:
        status = game['status']['short']
        if status == 'NS':
            return GameStatus.NOT_STARTED
        if status == 'FT':
            return GameStatus.FINAL
        return GameStatus.IN_PROGRESS
