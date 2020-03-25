import json
import os

import boto3

from swm.api_gateway_utils import get_query_params, buid_default_response
from swm.model.user import UserBuilder
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler

TABLE_ENV = 'USER_TABLE'
TABLE_ENV_DEFAULT = 'SWM_USERS'

LIMIT = 'limit'
LIMIT_DEFAULT = 50

PAGINATION_KEY = 'paginationKey'


@default_api_gw_handler
def handler(event, context):
    query_params = get_query_params(event)

    limit = query_params.get(LIMIT, LIMIT_DEFAULT)
    pagination_key = query_params.get(PAGINATION_KEY)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))

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

    return buid_default_response(
        status=200,
        body=json.dumps(
            {
                'paginationKey': query.get('LastEvaluatedKey'),
                'items': users
            },
            cls=SWMJSONEncoder
        )
    )
