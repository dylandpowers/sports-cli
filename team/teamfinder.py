from network.api import Api


class TeamFinder:
    """A service to team for and find a team based on a given team query"""
    def __init__(self, api_client: Api):
        self.api_client = api_client

    def find(self, search_term: str) -> int:
        """Searches for the team identified by the team term."""
        query_params = {
            'search': search_term
        }
        response_json = self.api_client.get('/teams', query_params)

        # only return the first team for now...
        return response_json['response'][0]['id']
