import os
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Attr

from swm.exception.business_exception import BusinessException
from swm.model.session import Session
from swm.model.user import UserType
from swm.model.userphoto import UserPhoto, UserPhotoBuilder

TABLE_ENV = 'USER_PHOTO_TABLE'
TABLE_ENV_DEFAULT = 'SWM_USER_PHOTO'


def get_user_photo(session: Session, oid_user: str):
    if not session or (session.user.oid != oid_user and session.user.type_ != UserType.ADMIN):
        raise BusinessException('Usuário não pode obter esta foto')

    table = _get_table()

    query = table.scan(FilterExpression=Attr('oid_user').eq(oid_user))

    items = query['Items']
    if len(items) > 0:
        item = items[0]
        return UserPhotoBuilder().from_json(item).build()


def update_user_photo(session: Session, oid_user: str, data: str):
    user_photo = get_user_photo(session, oid_user)
    if not user_photo:
        user_photo = UserPhoto()
        user_photo.oid_user = oid_user

    user_photo.data = data

    save(user_photo)

    return user_photo


def save(user_photo):
    table = _get_table()

    if not user_photo.created_at:
        user_photo.created_at = datetime.now()
    user_photo.updated_at = datetime.now()

    table.put_item(Item=user_photo.to_dict())


def _get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))
