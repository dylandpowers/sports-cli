#!/usr/bin/python
import argparse
from sportsrepository import SportsRepository

parser = argparse.ArgumentParser(description='A sports command line tool.')

parser.add_argument('-s', '--score', action='store_true', help='Fetch the score for a given team.')
parser.add_argument('-t', '--team', help='Specify a team name.')
parser.add_argument('-i', '--id', help='Specify a team id.')

args = parser.parse_args()

repository = SportsRepository()
if args.score:
    if not args.team and not args.id:
        print('Team or ID required to specify score.')
        quit(1)
    if args.id:
        print(repository.get_basketball_score(args.id))
