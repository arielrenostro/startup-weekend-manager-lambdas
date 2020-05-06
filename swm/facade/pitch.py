import os
from datetime import datetime
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr

from swm.business import pitch as PitchBusiness
from swm.model.pitch import Pitch, PitchBuilder
from swm.model.user import User

TABLE_ENV = 'PITCH_TABLE'
TABLE_ENV_DEFAULT = 'SWM_PITCH'


def list_pitchs(limit, pagination_key):
    table = _get_table()

    params = {
        'Limit': limit
    }
    if pagination_key:
        params['ExclusiveStartKey'] = pagination_key

    query = table.scan(**params)
    pitchs = []
    for item in query['Items']:
        pitch = _build_from_json(item)
        pitchs.append(pitch)

    return pitchs, query.get('LastEvaluatedKey')


def save(pitch: Pitch):
    table = _get_table()

    if not pitch.oid:
        pitch.oid = str(uuid4())
        pitch.created_at = datetime.now()
    pitch.updated_at = datetime.now()

    table.put_item(Item=pitch.to_dict())


def get_pitch_by_name(name):
    if name:
        table = _get_table()
        query = table.scan(
            FilterExpression=Attr('name').eq(name)
        )

        items = query['Items']
        if len(items) > 0:
            item = items[0]
            return _build_from_json(item)


def create_pitch(pitch: Pitch, oid_user: str):
    user = _get_user(oid_user)
    pitch_by_name = get_pitch_by_name(pitch.name)

    PitchBusiness.create_pitch(pitch, pitch_by_name, user) # TODO -> Validate current_phase to allow only in PITCH_TIME

    save(pitch)


def vote_pitch(oid_pitch, session):
    pitch = _get_pitch_by_oid(oid_pitch)

    from swm.facade import phase as PhaseFacade
    current_phase = PhaseFacade.get_current_phase()

    PitchBusiness.vote_pitch(pitch, session, current_phase)

    save(pitch)
    _save_user(session.real_user)


def _save_user(user):
    from swm.facade import user as UserFacade
    UserFacade.save(user)


def _get_pitch_by_oid(oid_pitch):
    table = _get_table()

    query = table.scan(
        FilterExpression=Attr('oid').eq(oid_pitch)
    )

    items = query['Items']
    if len(items) > 0:
        item = items[0]
        return _build_from_json(item)


def _get_user(oid_user) -> User:
    if oid_user:
        from swm.facade import user as UserFacade
        return UserFacade.get_user_by_oid(oid_user)


def _build_from_json(item):
    user = _get_user(item.get('oid_user'))

    pitch_builder = PitchBuilder().from_json(item)
    pitch_builder.with_user(user)
    return pitch_builder.build()


def _get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))

