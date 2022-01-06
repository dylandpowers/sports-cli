import fileinput
from os.path import exists

import inquirer

from . import TEAMFILE_NAME, Teams


def load() -> Teams:
    """Loads the team file."""
    with open(TEAMFILE_NAME, 'r') as f:
        teams = Teams()
        for i, line in enumerate(f.readlines()):
            data = line.split(":")
            if len(data) < 2:
                print('Line %d: please use the following format: <identifier>: <team_id>' % (i + 1))
                continue
            try:
                team_id = int(data[1].strip())
            except ValueError:
                print('Could not parse team id for identifier %s' % data[0])
                continue
            if data[0] == 'basketball':
                teams.set_basketball(team_id)
            # TODO(dpowers): implement rest of sports
    return teams


def try_save_selection(team_id: int, sport: str):
    """Tries to save the selection under the given sport to the team file."""
    option = inquirer.Confirm('save',
                              message='Would you like to save the current selection?\nThis will ' +
                                      'overwrite any existing selection for this sport.',
                              default=True)

    answers = inquirer.prompt([option])
    if answers['save']:
        # Create the file if it does not exist
        if not exists(TEAMFILE_NAME):
            with open(TEAMFILE_NAME, 'w') as f:
                f.write('%s: %d' % (sport, team_id))
        else:
            for line in fileinput.input(TEAMFILE_NAME, inplace=True):
                if sport in line:
                    print('%s: %d' % (sport, team_id))
                    return
            # If we get here, the line did not exist, so add it
            with open(TEAMFILE_NAME, 'a') as f:
                f.write('%s: %d' % (sport, team_id))
