import json

from swm.api_gateway_utils import buid_default_response, get_query_params
from swm.facade import pitch as PitchFacade
from swm.facade import session as SessionFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    query_params = get_query_params(event)
    oid_pitch = query_params.get('oid_pitch')

    session = SessionFacade.get_session_from_event(event)

    PitchFacade.vote_pitch(oid_pitch, session)

    return buid_default_response(
        status=200,
        body=json.dumps(
            {'vote': True},
            cls=SWMJSONEncoder
        )
    )


if __name__ == '__main__':
    print(
        handler(
            {
                'queryStringParameters': {
                    "oid_pitch": "cade9983-7df8-42eb-8c5d-0ba31a1056f4"
                },
                'requestContext': {
                    'authorizer': {
                        'jwt_payload': '{"type": "LOGGED","user": {"oid": "008bfdcf-85a9-460a-8d41-49ea23936a9c","name": "Ariel","email": "arielrenostro@gmail.com","cellphone": "47992181824","created_at": 1585099807,"updated_at": 1586914329,"type": "ADMIN"},"data": {},"exp": 1588123554,"nbf": 1588112703}'
                    }
                }
            },
            None
        )
    )
