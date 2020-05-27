from swm.api_gateway_utils import buid_default_response, get_jwt_cookie_value
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    return buid_default_response(
        status=200,
        headers={
            'Set-Cookie': get_jwt_cookie_value('')
        }
    )


if __name__ == '__main__':
    print(handler({}, None))
