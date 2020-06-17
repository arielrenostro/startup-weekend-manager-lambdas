import json

from swm.api_gateway_utils import buid_default_response, get_json_body, get_path_params
from swm.exception.request_exception import RequestException
from swm.facade import pitch as PitchFacade
from swm.model.pitch import PitchBuilder
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    body = get_json_body(event)
    if not body:
        raise RequestException("Request inválido!")

    path_params = get_path_params(event)
    oid = path_params.get('oid', None)
    if not oid:
        print(json.dumps(path_params))
        raise RequestException("ID inválido")

    pitch = PitchBuilder().from_json(body).build()

    oid_user = body.get('oid_user')
    PitchFacade.edit_pitch(oid, pitch, oid_user)

    return buid_default_response(
        status=201,
        body=json.dumps(
            pitch,
            cls=SWMJSONEncoder
        )
    )


if __name__ == '__main__':
    print(
        handler({'body': '{"name": "Gerenciador do evento", "oid_user": "008bfdcf-85a9-460a-8d41-49ea23936a9c"}', 'pathParameters': {'oid': 'cade9983-7df8-42eb-8c5d-0ba31a1056f4'}}, None)
    )
