from datetime import datetime, timedelta

import boto3
from jwt_rsa.token import JWT

from swm.api_gateway_utils import buid_default_response, get_jwt_cookie_value, get_json_body
from swm.exception.request_exception import RequestException
from swm.facade import otp as OTPFacade
from swm.facade import session as SessionFacade
from swm.facade import user as UserFacade
from swm.model.session import SessionBuilder, SessionType
from swm.wrapper.default_api_gw_handler import default_api_gw_handler

PRIVATE_KEY = '/SWM/Auth/PrivateCertificate'
PUBLIC_KEY = '/SWM/Auth/PublicCertificate'


def _get_ssm_value(ssm, key: str, decript: bool):
    parameter = ssm.get_parameter(Name=key, WithDecryption=decript)
    return parameter.get('Parameter', {}).get('Value')


def _generate_jwt_token(user):
    jwt = _create_jwt()

    session = SessionBuilder()\
        .with_type(SessionType.LOGGED)\
        .with_user(user)\
        .build()

    jwt_token = jwt.encode(
        **session.to_dict(),
        expired=(datetime.now() + timedelta(minutes=30)).timestamp(),
    )

    return jwt_token


def _create_jwt():
    ssm = boto3.client('ssm')
    private_key = _get_ssm_value(ssm, PRIVATE_KEY, True)
    public_key = _get_ssm_value(ssm, PUBLIC_KEY, True)
    jwt = JWT(
        private_key=private_key.encode(),
        public_key=public_key.encode()
    )
    return jwt


def _get_field_value_from_session(session):
    if 'cellphone' in session.data:
        return 'cellphone', session.data.get('cellphone')
    return 'email', session.data.get('email')


@default_api_gw_handler
def handler(event, context):
    session = SessionFacade.get_session_from_event(event)
    if not session or not session.data:
        raise RequestException('Sessão inválida')

    otp_hash = session.data.get('otp_hash')
    if not otp_hash:
        raise RequestException('Sessão inválida')

    otp_dto = OTPFacade.generate_code(otp_hash)

    body = get_json_body(event)
    otp_body = body.get('otp')

    if otp_dto.code != otp_body:
        print(f'Invalid OTP in check session {otp_dto.hex_}, {otp_dto.code}, body {otp_body}')
        raise RequestException('OTP inválido', 401)

    field, value = _get_field_value_from_session(session)

    user = UserFacade.get_user(field, value)
    if not user:
        print(f'User not exists {session.data}')
        raise RequestException('OTP inválido', 401)

    jwt_token = _generate_jwt_token(user)
    headers = {
        'Set-Cookie': get_jwt_cookie_value(jwt_token),
        'X-SWM-AUTHORIZATION': jwt_token
    }

    return buid_default_response(
        status=200,
        headers=headers
    )


if __name__ == '__main__':
    handler({'body': '{"otp": "2020"}'}, None)
