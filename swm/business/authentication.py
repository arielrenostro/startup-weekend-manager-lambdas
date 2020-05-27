import os

from swm.api_gateway_utils import get_path_request, get_method_request
from swm.exception.business_exception import BusinessException
from swm.model.session import SessionType, Session
from swm.model.user import UserType

ENDPOINTS_BY_SESSION_TYPE = {
    None: [
        '/v1/otp/request'
    ],
    SessionType.LOGGED: [
        '/v1/user',
        '/v1/pitch',
        '/v1/pitch/vote',
        '/v1/phase/current',
        '/v1/team',
        '/v1/logout'
    ],
    SessionType.OTP_REQUEST: [
        '/v1/otp/confirm',
        '/v1/otp/request'
    ]
}

ENDPOINTS_BY_USER_TYPE = {
    None: {
        '/v1/otp/confirm': '*',
        '/v1/otp/request': '*'
    },
    UserType.NORMAL: {
        '/v1/user': ['GET'],
        '/v1/pitch': ['GET'],
        '/v1/pitch/vote': ['PUT'],
        '/v1/phase/current': ['PUT'],
        '/v1/team': ['GET'],
        '/v1/logout': ['POST']
    }
}


def validate_user(event, session: Session):
    if session:
        path = get_path_request(event)
        method = get_method_request(event)

        user_type = session.user.type_ if session.user else None

        paths = ENDPOINTS_BY_USER_TYPE.get(user_type, {})
        method_by_path = paths.get(path, [])
        if method_by_path != '*' and method not in method_by_path:
            raise BusinessException(f'Usuário inválido para este endpoint! [user_type={user_type}, method={method}, path={path}]')


def validate_session(event, session: Session):
    path = get_path_request(event)

    session_type = session.type_ if session else None
    if path not in ENDPOINTS_BY_SESSION_TYPE.get(session_type, []):
        raise BusinessException(f'Sessão inválida para este endpoint! [path={path}, session_type={session_type}]')


def is_admin(session):
    user_type = session.user.type_ if session and session.user else None
    return UserType.ADMIN == user_type


def validate_authentication(event, session):
    if not is_admin(session):
        validate_session(event, session)
        validate_user(event, session)


def validate_jwt_fail(event, jwt_exception):
    path = get_path_request(event)
    if path not in ENDPOINTS_BY_SESSION_TYPE[None]:
        raise jwt_exception


def define_cors_headers(event, headers_to_define: dict):
    headers = event.get('headers', {})

    origin = headers.get('Origin', headers.get('origin'))
    print(f'header [Origin={origin}]')
    if not origin:
        origin = headers.get('Host', headers.get('host'))
        print(f'header [Host={origin}]')

    if not origin:
        origin = os.getenv('ORIGIN_DEFAULT')
        print(f'env [ORIGIN_DEFAULT={origin}]')

    if not origin:
        origin = '*'
        print(f'all origin')

    headers_to_define.update({
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE, HEAD',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-SWM-AUTHORIZATION,Cookie',
        'Access-Control-Max-Age': '1728000'
    })
