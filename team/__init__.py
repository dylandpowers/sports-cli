from pathlib import Path


TEAMFILE_NAME = str(Path.home()) + '/.Teamfile'

class Teams:
    """Model for representing data about a user's favorite teams"""
    def __init__(self):
        self.basketball = 0
        self.hockey = 0
        self.football = 0
        self.baseball = 0
        self.ncaam = 0

    def get_basketball(self):
        return self.basketball

    def set_basketball(self, team: int):
        self.basketball = team
