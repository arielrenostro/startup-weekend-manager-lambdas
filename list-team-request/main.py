import json

from swm.api_gateway_utils import buid_default_response
from swm.facade import session as SessionFacade
from swm.facade import teamrequest as TeamRequestFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    session = SessionFacade.get_session_from_event(event)

    team = TeamRequestFacade.get_team_by_oid(session.real_user.team.oid)
    if team is not None and team.leader.oid == session.user.oid:
        requests = TeamRequestFacade.get_requests_by_oid_team(session.real_user.team.oid)
    else:
        requests = TeamRequestFacade.get_requests_by_oid_user(session.user.oid)

    return buid_default_response(status=200, body=json.dumps(requests, cls=SWMJSONEncoder))


if __name__ == '__main__':
    print(
        handler(
            {
                'requestContext': {
                    'authorizer': {
                        'jwt_payload': '{"type": "LOGGED","user": {"oid": "008bfdcf-85a9-460a-8d41-49ea23936a9c","name": "Ariel","email": "arielrenostro@gmail.com","cellphone": "47992181824","created_at": 1585099807,"updated_at": 1586914329,"type": "ADMIN"},"data": {},"exp": 1588123554,"nbf": 1588112703}'
                    }
                }
            },
            None
        )
    )
