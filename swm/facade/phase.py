import os
from typing import List
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr

from swm.business import phase as PhaseBusiness
from swm.model.phase import Phase, PhaseBuilder
from swm.model.team import Team

TABLE_ENV = 'PHASE_TABLE'
TABLE_ENV_DEFAULT = 'SWM_PHASE'


def save(phase: Phase):
    table = _get_table()

    if not phase.oid:
        phase.oid = str(uuid4())

    table.put_item(Item=phase.to_dict())


def get_current_phase() -> Phase:
    table = _get_table()
    query = table.scan(
        FilterExpression=Attr('selected').eq(True)
    )

    items = query['Items']
    if len(items) > 0:
        item = items[0]
        return PhaseBuilder().from_json(item).build()


def next_phase():
    current_phase = get_current_phase()
    next_phase_ = PhaseBusiness.next_phase(current_phase)
    return select_phase_by_name(next_phase_.name)


def list_phases() -> List[Phase]:
    return PhaseBusiness.list_phases()


def select_phase_by_name(phase_name):
    def _current_phase_provider():
        return get_current_phase()

    old_phase, new_phase = PhaseBusiness.select_phase_by_name(phase_name, _current_phase_provider)

    message = None
    if old_phase:
        message = process_phase_change(old_phase, new_phase)
        save(old_phase)
    save(new_phase)

    return old_phase, new_phase, message


def process_phase_change(current_phase: Phase, phase: Phase):
    if PhaseBusiness.VOTE_PITCH == current_phase.name:
        return process_vote_pitch()

    elif PhaseBusiness.ASSEMBLING_TEAMS == current_phase.name:
        return process_assembling_teams()


def process_assembling_teams():
    def _get_user_by_id(users_, member_):
        for user_ in users_:
            if user_.oid == member_.oid:
                return user_

    def _link_user_in_team(users_to_save_, teams_to_save_, users_, teams_):
        for team_ in teams_:
            if len(users_) == 0:
                break
            user_ = users_.pop(0)
            user_.team = team_
            team_.members.append(user_)

            users_to_save_.append(user_)
            teams_to_save_.append(team_)

    from swm.facade import user as UserFacade
    from swm.facade import team as TeamFacade

    teams, _ = TeamFacade.list_teams(1000000, None)
    users, _ = UserFacade.list_users(1000000, None)

    for team in teams:
        for member in team.members:
            user = _get_user_by_id(users, member)
            if user:
                users.remove(user)

    users_to_save = []
    teams_to_save = []

    teams_non_completed = TeamFacade.get_non_completed_teams(teams)
    _link_user_in_team(users_to_save, teams_to_save, users, teams_non_completed)

    while len(users) > 0:
        _link_user_in_team(users_to_save, teams_to_save, users, teams)

    for team in teams_to_save:
        TeamFacade.save(team)

    for user in users_to_save:
        UserFacade.save(user)

    return "Equipes montadas e todos os usuários foram vinculados em alguma equipe"


def process_vote_pitch():
    from swm.facade import user as UserFacade
    from swm.facade import team as TeamFacade
    from swm.facade import pitch as PitchFacade

    users, _ = UserFacade.list_users(1000000, None)
    pitchs, _ = PitchFacade.list_pitchs(1000000, None)

    pitchs.sort(key=lambda x: len(x.votes), reverse=True)

    created_teams = []
    teams_amount = int(len(users) / TeamFacade.TEAMS_SIZE)
    if len(users) % TeamFacade.TEAMS_SIZE > 0:
        teams_amount += 1

    for i in range(teams_amount):
        if i >= len(pitchs):
            break

        pitch = pitchs[i]
        pitch.approved = True

        team = Team()
        created_teams.append(team)

        user = pitch.user
        user.team = team

        team.name = pitch.name
        team.leader = user
        team.members = [user]

        PitchFacade.save(pitch)
        TeamFacade.save(team)
        UserFacade.save(user)

    return f"Criadas as equipes: {', '.join(list(map(lambda x: x.name, created_teams)))}"


def is_judges_vote() -> bool:
    phase = get_current_phase()
    return PhaseBusiness.is_jugdes_vote(phase)


def _get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))
