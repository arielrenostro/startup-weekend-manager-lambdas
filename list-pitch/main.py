import json

from swm.api_gateway_utils import get_query_params, buid_default_response
from swm.facade import pitch as PitchFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler

LIMIT = 'limit'
LIMIT_DEFAULT = 50

PAGINATION_KEY = 'paginationKey'


@default_api_gw_handler
def handler(event, context):
    query_params = get_query_params(event)

    limit = query_params.get(LIMIT, LIMIT_DEFAULT)
    pagination_key = query_params.get(PAGINATION_KEY, {})

    pitchs, last_evaluated_key = PitchFacade.list_pitchs(limit, pagination_key)

    return buid_default_response(
        status=200,
        body=json.dumps(
            {
                'paginationKey': last_evaluated_key,
                'items': pitchs
            },
            cls=SWMJSONEncoder
        )
    )


if __name__ == '__main__':
    print(handler({'body': ''}, None))
