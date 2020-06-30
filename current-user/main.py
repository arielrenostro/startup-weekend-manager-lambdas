import json

from swm.api_gateway_utils import buid_default_response
from swm.facade import session as SessionFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    session = SessionFacade.get_session_from_event(event)
    user = session.real_user

    json_body = user.to_dict()
    json_body.pop('password')
    json_body.pop('oid_team')
    json_body['team'] = user.team

    return buid_default_response(
        status=200,
        body=json.dumps(
            json_body,
            cls=SWMJSONEncoder
        )
    )


if __name__ == '__main__':
    print(handler({'body': ''}, None))
