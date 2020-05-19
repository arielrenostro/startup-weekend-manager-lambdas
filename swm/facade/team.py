import os
from datetime import datetime
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr

from swm.business import team as TeamBusiness
from swm.model.team import TeamBuilder, Team

TABLE_ENV = 'TEAM_TABLE'
TABLE_ENV_DEFAULT = 'SWM_TEAM'

TEAMS_SIZE = TeamBusiness.TEAMS_SIZE


def list_teams(limit, pagination_key):  # TODO -> Implementar validação para restringir tamanho de equipe
    table = _get_table()

    params = {
        'Limit': limit
    }
    if pagination_key:
        params['ExclusiveStartKey'] = pagination_key

    query = table.scan(**params)
    teams = []
    for item in query['Items']:
        team = _build_from_json(item, load_users=True)
        teams.append(team)

    return teams, query.get('LastEvaluatedKey')


def get_team_by_oid(oid_team, load_users=True):
    table = _get_table()

    query = table.scan(
        FilterExpression=Attr('oid').eq(oid_team)
    )

    items = query['Items']
    if len(items) > 0:
        return _build_from_json(items[0], load_users=load_users)


def save(team: Team):
    table = _get_table()

    if not team.oid:
        team.oid = str(uuid4())
        team.created_at = datetime.now()
    team.updated_at = datetime.now()

    table.put_item(Item=team.to_dict())


def get_non_completed_teams(teams):
    return TeamBusiness.get_non_completed_teams(teams)


def _build_from_json(item, load_users):
    team = TeamBuilder().from_json(item).build()
    # Overrides the "TempUser" for the real user
    if load_users:
        from swm.facade import user as UserFacade
        if team.leader:
            team.leader = UserFacade.get_user_by_oid(team.leader.oid, load_team=False)
        if team.members:
            team.members = [UserFacade.get_user_by_oid(m.oid, load_team=False) for m in team.members]
    return team


def _get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))
