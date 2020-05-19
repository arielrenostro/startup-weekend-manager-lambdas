from typing import List

from swm.model.team import Team

TEAMS_SIZE = 5


def get_non_completed_teams(teams: List[Team]):
    result = []
    for team in teams:
        if len(team.members) < TEAMS_SIZE:
            result.append(team)
    return result
