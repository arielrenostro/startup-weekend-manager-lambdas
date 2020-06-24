import json

from swm.api_gateway_utils import buid_default_response, get_json_body
from swm.exception.request_exception import RequestException
from swm.facade import session as SessionFacade
from swm.facade import teamrequest as TeamRequestFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    body = get_json_body(event)
    if not body:
        raise RequestException("Request inválido!")

    oid_team = body.get('oid_team')
    if not oid_team:
        raise RequestException("Time não informado")

    session = SessionFacade.get_session_from_event(event)

    team_request = TeamRequestFacade.create_new_request(session.real_user, oid_team)

    return buid_default_response(status=201, body=json.dumps(team_request, cls=SWMJSONEncoder))


if __name__ == '__main__':
    print(
        handler(
            {
                'body': '{"oid_team": "dbf90238-a1be-471a-8422-4782294cd7a7"}',
                'requestContext': {
                    'authorizer': {
                        'jwt_payload': '{"type": "LOGGED","user": {"oid": "008bfdcf-85a9-460a-8d41-49ea23936a9c","name": "Ariel","email": "arielrenostro@gmail.com","cellphone": "47992181824","created_at": 1585099807,"updated_at": 1586914329,"type": "ADMIN"},"data": {},"exp": 1588123554,"nbf": 1588112703}'
                    }
                }
            },
            None
        )
    )
