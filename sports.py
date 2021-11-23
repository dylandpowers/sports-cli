#!/usr/bin/env python3
import argparse
import os
from os.path import exists

from network.api import Api
from team import TEAMFILE_NAME
from team.teamfileloader import load
from team.teamfinder import TeamFinder
from gamerepository import GameRepository

api_key = os.getenv('X_RAPIDAPI_KEY')
if not api_key:
    print('Please export an environment variable X_RAPIDAPI_KEY')
    quit(1)

parser = argparse.ArgumentParser(description='A sports command line tool.')

parser.add_argument('-s', '--score', action='store_true', help='Fetch the score for a given team.')
parser.add_argument('-t', '--team', help='Specify a team name.')
parser.add_argument('-i', '--id', help='Specify a team id.')

args = parser.parse_args()

api_client = Api(api_key)
repository = GameRepository(api_client)
finder = TeamFinder(api_client)
if args.score:
    if not args.team and not args.id:
        if not exists(TEAMFILE_NAME):
            print("Must specify either a team name or id, or declare a .Sportsfile in the home dir")
            exit(1)
        teams = load()

        if teams.get_basketball():
            print(repository.get_basketball_score(teams.get_basketball()))
    elif args.id:
        print(repository.get_basketball_score(args.id))
    else:
        team_id = finder.find(args.team)
        if not team_id:
            print('Could not find any team matching the given search term.')
            quit(1)
        print(repository.get_basketball_score(team_id))
