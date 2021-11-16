class Score:
    def __init__(self, home_name=None, away_name=None, home_score=None, away_score=None,
                 errors=None):
        self.home_name = home_name
        self.away_name = away_name
        self.home_score = home_score
        self.away_score = away_score
        self.errors = errors if errors else []

    def __repr__(self):
        return "%-30s%s\n%-30s%s" % (self.away_name, self.away_score, self.home_name, self.home_score)