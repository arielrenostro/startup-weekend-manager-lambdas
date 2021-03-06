import json

from swm.api_gateway_utils import buid_default_response, get_json_body
from swm.exception.request_exception import RequestException
from swm.facade import user as UserFacade
from swm.model.user import UserBuilder
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    body = get_json_body(event)
    if not body:
        raise RequestException("Request inválido!")

    user = UserBuilder().from_json(body, encrypt_password=True).build()

    UserFacade.create_user(user)

    return buid_default_response(
        status=201,
        body=json.dumps(
            user,
            cls=SWMJSONEncoder
        )
    )


if __name__ == '__main__':
    print(
        handler({'body': '{"name": "Ruan", "email": "schuartzrussi@gmail.com", "cellphone": "47991979914", "password": "123456"}'}, None)
    )
