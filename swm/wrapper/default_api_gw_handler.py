import json
import traceback
from functools import wraps

from swm.api_gateway_utils import buid_default_response, get_jwt_from_authorizer, get_jwt_cookie_value
from swm.business import authentication as AuthenticationBusiness
from swm.context import current
from swm.exception.request_exception import RequestException


def define_headers(response, jwt):
    headers = response.get('headers', {})
    response['headers'] = headers

    if jwt:
        if 'X-SWM-AUTHORIZATION' not in headers:
            headers['X-SWM-AUTHORIZATION'] = jwt

        if 'Set-Cookie' not in headers:
            headers['Set-Cookie'] = get_jwt_cookie_value(jwt)

    AuthenticationBusiness.define_cors_headers(current.CURRENT_EVENT, headers)


def default_api_gw_handler(func):
    @wraps(func)
    def default_api_gw_handler_call(*args, **kwargs):
        event = kwargs.get('event')
        if not event and len(args) > 0 and isinstance(args[0], dict):
            event = args[0]

        current.CURRENT_EVENT = event

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
            traceback.print_exc()
            response = buid_default_response(
                status=500,
                body=json.dumps({
                    'ok': False,
                    'message': str(e)
                })
            )

        jwt = get_jwt_from_authorizer(event)
        define_headers(response, jwt)

        return response

    return default_api_gw_handler_call
