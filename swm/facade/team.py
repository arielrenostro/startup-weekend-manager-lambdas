import os

import boto3
from boto3.dynamodb.conditions import Attr

from swm.model.team import TeamBuilder

TABLE_ENV = 'TEAM_TABLE'
TABLE_ENV_DEFAULT = 'SWM_TEAM'


def list_teams(limit, pagination_key):
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
        return _build_from_json(items, load_users=load_users)


def _build_from_json(items, load_users):
    team = TeamBuilder().from_json(items[0]).build()
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
