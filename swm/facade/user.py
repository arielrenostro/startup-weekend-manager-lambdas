import os

import boto3
from boto3.dynamodb.conditions import Attr

from swm.model.user import UserBuilder

TABLE_ENV = 'USER_TABLE'
TABLE_ENV_DEFAULT = 'SWM_USERS'


def get_user(field, value):
    table = _get_table()

    query = table.scan(
        Limit=1,
        FilterExpression=Attr(field).eq(value)
    )

    items = query['Items']
    if len(items) > 0:
        return UserBuilder().from_json(items[0]).build()


def get_user_from_email(email):
    return get_user('email', email)


def get_user_from_cellphone(cellphone):
    return get_user('cellphone', cellphone)


def list_users(limit, pagination_key):
    table = _get_table()

    params = {
        'Limit': limit
    }
    if pagination_key:
        params['ExclusiveStartKey'] = pagination_key

    query = table.scan(**params)
    users = []
    for item in query['Items']:
        user_ = UserBuilder().from_json(item).build()
        users.append(user_)

    return users, query.get('LastEvaluatedKey')


def _get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))
