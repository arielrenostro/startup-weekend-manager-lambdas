import os
from datetime import datetime
from typing import List
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr

from swm.business import teamrequest as TeamRequestBusiness
from swm.facade import phase as PhaseFacade
from swm.facade import team as TeamFacade
from swm.facade import user as UserFacade
from swm.model.teamrequest import TeamRequestBuilder, TeamRequest, TeamRequestStatus
from swm.model.user import User

TABLE_ENV = 'TEAM_REQUEST_TABLE'
TABLE_ENV_DEFAULT = 'SWM_TEAM_REQUEST'


def get_by_oid(oid_team_request: str) -> TeamRequest:
    table = _get_table()
    query = table.scan(
        FilterExpression=Attr('oid').eq(oid_team_request)
    )

    items = query['Items']
    if len(items) > 0:
        return TeamRequestBuilder().from_json(items[0]).build()


def get_requests_by_oid_user(oid_user) -> List[TeamRequest]:
    table = _get_table()
    query = table.scan(
        FilterExpression=Attr('oid_user').eq(oid_user)
    )

    items = query['Items']
    if len(items) > 0:
        return [TeamRequestBuilder().from_json(item).build() for item in items]
    return []


def get_requests_by_oid_team(oid_team) -> List[TeamRequest]:
    table = _get_table()
    query = table.scan(
        FilterExpression=Attr('oid_team').eq(oid_team)
    )

    items = query['Items']
    if len(items) > 0:
        return [TeamRequestBuilder().from_json(item).build() for item in items]
    return []


def create_new_request(user: User, oid_team) -> TeamRequest:
    def _get_requests_by_oid_user_provider(_oid):
        return get_requests_by_oid_user(_oid)

    def _get_team_provider(_oid):
        return TeamFacade.get_team_by_oid(_oid, load_users=False)

    current_phase = PhaseFacade.get_current_phase()

    TeamRequestBusiness.validate_new_request(
        user,
        oid_team,
        current_phase,
        _get_requests_by_oid_user_provider,
        _get_team_provider
    )

    team_request = TeamRequest()
    team_request.status = TeamRequestStatus.PENDING
    team_request.oid_user = user.oid
    team_request.oid_team = oid_team

    save(team_request)

    return team_request


def approve_request(user: User, oid_team_request: str):
    def _get_user_provider(_oid):
        return UserFacade.get_user_by_oid(_oid)

    def _get_team_provider(_oid):
        return TeamFacade.get_team_by_oid(_oid)

    team_request = get_by_oid(oid_team_request)
    user, team = TeamRequestBusiness.approve_request(team_request, user, _get_user_provider, _get_team_provider)

    save(team_request)
    UserFacade.save(user)
    TeamFacade.save(team)

    return team_request


def reject_request(user: User, oid_team_request: str):
    team_request = get_by_oid(oid_team_request)
    TeamRequestBusiness.reject_request(team_request, user)

    save(team_request)

    return team_request


def get_team_by_oid(oid):
    return TeamFacade.get_team_by_oid(oid)


def save(team_request: TeamRequest):
    table = _get_table()

    if not team_request.oid:
        team_request.oid = str(uuid4())
        team_request.created_at = datetime.now()
    team_request.updated_at = datetime.now()

    table.put_item(Item=team_request.to_dict())


def _get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))
