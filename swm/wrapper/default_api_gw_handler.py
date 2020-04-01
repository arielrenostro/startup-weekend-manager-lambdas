import json
from functools import wraps

from swm.api_gateway_utils import buid_default_response, get_jwt_from_authorizer, define_set_cookie_header
from swm.exception.request_exception import RequestException


def default_api_gw_handler(func):
    @wraps(func)
    def default_api_gw_handler_call(*args, **kwargs):
        try:
            response = func(*args, **kwargs)

        except RequestException as e:
            response = buid_default_response(
                status=e.status_code,
                body=json.dumps({
                    'ok': False,
                    'message': e.message
                })
            )

        except Exception as e:
            response = buid_default_response(
                status=500,
                body=json.dumps({
                    'ok': False,
                    'message': str(e)
                })
            )

        event = kwargs.get('event')
        if not event and len(args) > 0 and isinstance(args[0], dict):
            event = args[0]

        jwt = get_jwt_from_authorizer(event)
        if jwt:
            define_set_cookie_header(response, jwt)

        return response
    return default_api_gw_handler_call
