from enum import Enum


class GameStatus(Enum):
    NOT_STARTED = 1
    NO_GAME = 2
    IN_PROGRESS = 3
    FINAL = 4


class Game:
    def __init__(self,
                 game_status=GameStatus.NOT_STARTED,
                 home_name=None,
                 away_name=None,
                 home_score=None,
                 away_score=None,
                 game_time=None):
        self.game_status = game_status
        self.home_name = home_name
        self.away_name = away_name
        self.home_score = home_score
        self.away_score = away_score
        self.game_time = game_time

    def __repr__(self):
        if self.game_status == GameStatus.NO_GAME:
            return "No game today."
        if self.game_status == GameStatus.NOT_STARTED:
            return "%s\n%-30s%s" % (self.away_name, self.home_name, self.game_time)
        return "%s\n%-30s%s\n%-30s%s" % \
               (self.game_time, self.away_name, self.away_score, self.home_name, self.home_score)
