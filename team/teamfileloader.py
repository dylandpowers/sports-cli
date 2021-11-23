from . import TEAMFILE_NAME, Teams


def load() -> Teams:
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
