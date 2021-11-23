import inquirer

from network.api import Api


class TeamFinder:
    NONE_OPTION = 'None of these'
    """
    A service to find a team based on a given team query. The service will also require input from
    the user to determine the correct id based on the search term.
    """

    def __init__(self, api_client: Api):
        self.api_client = api_client

    def find(self, search_term: str) -> int:
        """Searches for the team identified by the team term."""
        query_params = {
            'search': search_term
        }
        response_json = self.api_client.get('/teams', query_params)
        if not response_json['response']:
            return 0

        team_name_to_id = {team['name']: team['id'] for team in response_json['response']}
        team_names = list(team_name_to_id.keys())
        team_names.append(self.NONE_OPTION)

        option = inquirer.List('team',
                               message='Please select the correct team',
                               choices=team_names)

        answers = inquirer.prompt([option])
        if answers['team'] == self.NONE_OPTION:
            return 0

        return team_name_to_id[answers['team']]
