import json

from swm.api_gateway_utils import buid_default_response, get_json_body
from swm.exception.request_exception import RequestException
from swm.facade import team as TeamFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    body = get_json_body(event)
    if not body:
        raise RequestException("Request inválido!")

    if not isinstance(body, list):
        raise RequestException("Esperado uma lista!")

    teams = TeamFacade.define_teams_position(body)

    return buid_default_response(
        status=200,
        body=json.dumps(
            teams,
            cls=SWMJSONEncoder
        )
    )


if __name__ == '__main__':
    print(
        handler({'body': '{"name": "Teste", "oid_user": "008bfdcf-85a9-460a-8d41-49ea23936a9c"}'}, None)
    )
