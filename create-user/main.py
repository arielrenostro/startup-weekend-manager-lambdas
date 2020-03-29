import json
import os
from datetime import datetime
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr, Or

from swm.api_gateway_utils import buid_default_response, get_json_body
from swm.exception.request_exception import RequestException
from swm.model.user import UserBuilder
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler

TABLE_ENV = 'USER_TABLE'
TABLE_ENV_DEFAULT = 'SWM_USERS'


def get_user_from_body(body):
    user = UserBuilder().from_json(body, encrypt_password=True).build()
    if user.oid:
        raise RequestException("OID deve ser gerado dinamicamente")
    if not user.password:
        raise RequestException("Campo 'password' é obrigatório")
    if not user.cellphone:
        raise RequestException("Campo 'cellphone' é obrigatório")
    return user


def validate_duplicated_user(table, user):
    query = table.scan(
        Limit=1,
        FilterExpression=Or(
            Attr('email').eq(user.email),
            Attr('cellphone').eq(user.cellphone)
        )
    )
    if len(query['Items']) > 0:
        raise RequestException('Já existe um usuário com o mesmo telefone ou e-mail')


@default_api_gw_handler
def handler(event, context):
    body = get_json_body(event)
    if not body:
        raise RequestException("Request inválido!")

    user = get_user_from_body(body)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))

    validate_duplicated_user(table, user)

    user.oid = str(uuid4())
    user.created_at = datetime.now()
    user.updated_at = datetime.now()

    table.put_item(Item=user.to_json())

    return buid_default_response(
        status=201,
        body=json.dumps(
            user,
            cls=SWMJSONEncoder
        )
    )

