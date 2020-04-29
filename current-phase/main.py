import json

from swm.api_gateway_utils import buid_default_response
from swm.facade import phase as PhaseFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler

LIMIT = 'limit'
LIMIT_DEFAULT = 50

PAGINATION_KEY = 'paginationKey'


@default_api_gw_handler
def handler(event, context):
    current_phase = PhaseFacade.get_current_phase()

    return buid_default_response(
        status=200,
        body=json.dumps(
            current_phase,
            cls=SWMJSONEncoder
        )
    )


if __name__ == '__main__':
    print(handler({'body': ''}, None))
