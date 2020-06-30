import json
from http import cookies


def get_json_body(event) -> dict:
    body = event.get('body')
    if body:
        try:
            return json.loads(body)
        except:
            pass
    return {}


def get_headers(event) -> dict:
    headers = event.get('headers')
    if headers:
        return headers
    return {}


def get_query_params(event) -> dict:
    query_params = event.get('queryStringParameters')
    if query_params:
        return query_params
    return {}


def get_path_params(event) -> dict:
    path_params = event.get('pathParameters')
    if path_params:
        return path_params
    return {}


def get_authorizer(event) -> dict:
    request_context = event.get('requestContext')
    if request_context:
        authorizer = request_context.get('authorizer')
        if authorizer:
            return authorizer
    return {}


def get_path_request(event) -> str:
    path = event.get('path')
    if path:
        return path
    return ''


def get_resource_request(event) -> str:
    resource = event.get('resource')
    if resource:
        return resource
    return ''


def get_method_request(event) -> str:
    method = event.get('httpMethod')
    if method:
        return method
    return ''


def get_jwt_from_authorizer(event) -> str:
    authorizer = get_authorizer(event)
    jwt = authorizer.get('jwt')
    if jwt:
        return jwt
    return ''


def get_jwt_payload(event) -> dict:
    authorizer = get_authorizer(event)
    payload = authorizer.get('jwt_payload')
    if payload:
        return json.loads(payload)
    return {}


def get_jwt_cookie_value(jwt):
    cookie = cookies.SimpleCookie()
    cookie['jwt'] = jwt
    cookie['jwt']['httponly'] = True
    cookie['jwt']['path'] = '/'
    cookie['jwt']['secure'] = 'true'
    return cookie.output().split(':')[1].strip()


def buid_default_response(status: int = None, body: str = None, headers: dict = None, base64encoded: bool = False):
    if not status:
        status = 200

    if not headers:
        headers = {}

    if not body:
        body = "{}"

    if not headers.get('Content-Type'):
        headers['Content-Type'] = 'application/json'

    return {
        'statusCode': status,
        'body': body,
        'headers': headers,
        'isBase64Encoded': base64encoded,
    }
