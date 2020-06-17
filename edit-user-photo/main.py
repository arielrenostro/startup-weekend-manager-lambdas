import json

from swm.api_gateway_utils import buid_default_response, get_path_params
from swm.exception.request_exception import RequestException
from swm.facade import session as SessionFacade
from swm.facade import userphoto as UserPhotoFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    body = event.get('body')
    if not body:
        raise RequestException("Request inválido!")

    path_params = get_path_params(event)
    oid = path_params.get('oid', None)
    if not oid:
        print(json.dumps(path_params))
        raise RequestException("ID inválido")

    session = SessionFacade.get_session_from_event(event)

    user_photo = UserPhotoFacade.update_user_photo(session, oid, body)

    return buid_default_response(
        status=200,
        body=json.dumps(
            user_photo,
            cls=SWMJSONEncoder
        )
    )
