import json

from swm.exception.request_exception import RequestException


def get_json_body(event) -> dict:
    body = event.get('body')
    if body:
        try:
            return json.loads(body)
        except:
            pass


def get_headers(event) -> dict:
    return event.get('headers', {})


def get_query_params(event) -> dict:
    return event.get('queryStringParameters', {})


def default_api_gw_handler(func):
    def default_api_gw_handler_call(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except RequestException as e:
            return buid_default_response(
                status=400,
                body=json.dumps({
                    'ok': False,
                    'message': e.message
                })
            )
    return default_api_gw_handler_call


def buid_default_response(status: int = None, body: str = None, headers: dict = None):
    if not status:
        status = 200

    if not headers:
        headers = {}

    if not body:
        body = "{}"

    if not headers.get('Content-Type'):
        headers['Content-Type'] = 'application/json'

    if not headers.get('Access-Control-Allow-Origin'):
        headers['Access-Control-Allow-Origin'] = '*'

    return {
        'statusCode': status,
        'body': body,
        'headers': headers
    }
