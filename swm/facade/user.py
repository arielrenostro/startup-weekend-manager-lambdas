import os
from datetime import datetime
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr

from swm.business import user as UserBusiness
from swm.model.user import UserBuilder

TABLE_ENV = 'USER_TABLE'
TABLE_ENV_DEFAULT = 'SWM_USERS'


def get_user(field, value):
    table = _get_table()

    query = table.scan(
        FilterExpression=Attr(field).eq(value)
    )

    items = query['Items']
    if len(items) > 0:
        return UserBuilder().from_json(items[0]).build()


def get_user_by_email(email):
    return get_user('email', email)


def get_user_by_cellphone(cellphone):
    return get_user('cellphone', cellphone)


def get_user_by_oid(oid):
    return get_user('oid', oid)


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


def save(user):
    table = _get_table()

    if not user.oid:
        user.oid = str(uuid4())
        user.created_at = datetime.now()
    user.updated_at = datetime.now()

    table.put_item(Item=user.to_dict())


def create_user(user):
    user_by_email = get_user_by_email(user.email)
    user_by_cellphone = get_user_by_cellphone(user.cellphone)

    UserBusiness.create_user(user, user_by_cellphone, user_by_email)

    save(user)


def _get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))
