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
        handler({'body': '{"name": "Teste", "oid_user": "008bfdcf-85a9-460a-8d41-49ea23936a9c"}'}, None)
    )
