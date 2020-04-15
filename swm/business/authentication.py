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
        '/v1/pitch'
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
        '/v1/pitch': ['GET']
    },
    UserType.ADMIN: {
        '/v1/pitch': '*'
    }
}


def validate_user(event, session: Session):
    if session:
        path = get_path_request(event)
        method = get_method_request(event)

        user_type = session.user.type_ if session.user else None

        paths = ENDPOINTS_BY_USER_TYPE.get(user_type, {})
        method_by_path = paths.get(path, [])
        if UserType.ADMIN != user_type and method_by_path != '*' and method not in method_by_path:
            raise BusinessException('Usuário inválido para este endpoint!')


def validate_session(event, session: Session):
    path = get_path_request(event)

    session_type = session.type_ if session else None
    if path not in ENDPOINTS_BY_SESSION_TYPE.get(session_type, []):
        raise BusinessException('Sessão inválida para este endpoint!')


def validate_authentication(event, session):
    validate_session(event, session)
    validate_user(event, session)


def validate_jwt_fail(event, jwt_exception):
    path = get_path_request(event)
    if path not in ENDPOINTS_BY_SESSION_TYPE[None]:
        raise jwt_exception
