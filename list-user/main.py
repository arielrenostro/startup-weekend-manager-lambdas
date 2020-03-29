import json
import os

import boto3

from swm.api_gateway_utils import get_query_params, default_api_gw_handler
from swm.model.user import UserBuilder
from swm.swm_json_encoder import SWMJSONEncoder

TABLE_ENV = 'USER_TABLE'
TABLE_ENV_DEFAULT = 'SWM_USERS'

LIMIT = 'limit'
LIMIT_DEFAULT = 50

PAGINATION_KEY = 'paginationKey'


@default_api_gw_handler
def handler(event, context):
    query_params = get_query_params(event)

    limit = query_params.get(LIMIT, LIMIT_DEFAULT)
    pagination_key = query_params.get(PAGINATION_KEY, {})

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))

    query = table.scan(Limit=limit, ExclusiveStartKey=pagination_key)

    users = []
    for item in query['Items']:
        user_ = UserBuilder().from_dynamodb(item).build()
        users.append(user_)

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                'paginationKey': query['LastEvaluatedKey'],
                'items': users
            },
            cls=SWMJSONEncoder
        ),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
