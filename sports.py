#!/usr/bin/env python3
import argparse
from datetime import date
import os
import re
from os.path import exists

from network.api import Api
from team import TEAMFILE_NAME
from team.teamfile import load, try_save_selection
from team.teamfinder import TeamFinder
from gamerepository import GameRepository

api_key = os.getenv('X_RAPIDAPI_KEY')
if not api_key:
    print('Please export an environment variable X_RAPIDAPI_KEY')
    quit(1)

parser = argparse.ArgumentParser(description='A command line tool for fetching sports data.')

DATE_REGEX = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')

parser.add_argument('-s', '--score', action='store_true', help='Fetch the score for a given team.')
parser.add_argument('-d', '--date', help='Specify a date in the format YYYY-MM-DD')
parser.add_argument('-t', '--team', help='Specify a team name.')
parser.add_argument('-i', '--id', help='Specify a team id.')

args = parser.parse_args()

api_client = Api(api_key)
repository = GameRepository(api_client)
finder = TeamFinder(api_client)
if args.score:
    if args.date:
        if not DATE_REGEX.match(args.date):
            print("Date must be in format: YYYY-MM-DD")
            exit(1)
        date_arg = args.date
    else:
        date_arg = date.today().strftime("%Y-%m-%d")

    if not args.team and not args.id:
        if not exists(TEAMFILE_NAME):
            print("Must specify either a team name or id, or declare a .Sportsfile in the home dir")
            exit(1)
        teams = load()

        if teams.get_basketball():
            print(repository.get_basketball_score(teams.get_basketball(), date_arg))
    elif args.id:
        print(repository.get_basketball_score(args.id, date_arg))
    else:
        team_id = finder.find(args.team)
        if not team_id:
            print('Could not find any team matching the given search term.')
            quit(1)
        print(repository.get_basketball_score(team_id))
        try_save_selection(team_id, 'basketball')
elif args.team or args.id:
    print("Please specify -s to get scores.")
    exit(1)
