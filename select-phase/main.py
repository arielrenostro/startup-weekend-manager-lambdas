import json

from swm.api_gateway_utils import buid_default_response, get_json_body
from swm.facade import phase as PhaseFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler

LIMIT = 'limit'
LIMIT_DEFAULT = 50

PAGINATION_KEY = 'paginationKey'


@default_api_gw_handler
def handler(event, context):
    body = get_json_body(event)
    phase_name = body.get('phase')

    old_phase, actual_phase = PhaseFacade.select_phase_by_name(phase_name)

    return buid_default_response(
        status=200,
        body=json.dumps({
            'oldPhase': old_phase,
            'actualPhase': actual_phase
        },
            cls=SWMJSONEncoder
        )
    )


if __name__ == '__main__':
    print(handler({'body': ''}, None))
