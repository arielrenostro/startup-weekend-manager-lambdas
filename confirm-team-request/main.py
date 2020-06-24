import json

from swm.api_gateway_utils import buid_default_response, get_path_params
from swm.exception.request_exception import RequestException
from swm.facade import session as SessionFacade
from swm.facade import teamrequest as TeamRequestFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    path_params = get_path_params(event)
    if not path_params:
        raise RequestException("Request inválido!")

    oid_request_team = path_params.get('oid')
    if not oid_request_team:
        raise RequestException("Solicitação de entrada no time não informado")

    session = SessionFacade.get_session_from_event(event)

    team_request = TeamRequestFacade.approve_request(session.real_user, oid_request_team)

    return buid_default_response(status=200, body=json.dumps(team_request, cls=SWMJSONEncoder))


if __name__ == '__main__':
    print(
        handler(
            {
                'pathParameters': {"oid": "e64d310a-fdb9-40b7-af5e-ac9e648dfeb1"},
                'requestContext': {
                    'authorizer': {
                        'jwt_payload': '{"type": "LOGGED","user": {"oid": "008bfdcf-85a9-460a-8d41-49ea23936a9c","name": "Ariel","email": "arielrenostro@gmail.com","cellphone": "47992181824","created_at": 1585099807,"updated_at": 1586914329,"type": "ADMIN"},"data": {},"exp": 1588123554,"nbf": 1588112703}'
                    }
                }
            },
            None
        )
    )
