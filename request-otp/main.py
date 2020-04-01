import json
import os
from datetime import datetime, timedelta

import boto3
from jwt_rsa.token import JWT
from totalvoice.cliente import Cliente

from swm.api_gateway_utils import buid_default_response, get_json_body, get_jwt_cookie_value
from swm.exception.request_exception import RequestException
from swm.facade import otp as OTPFacade
from swm.facade import user as UserFacade
from swm.model.session import SessionBuilder, SessionType
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler

SEND_SMS_DISABLED = 'SEND_SMS_DISABLED'

TOTALVOICE_TOKEN = 'TOTALVOICE_TOKEN'
TOTALVOICE_HOST = 'TOTALVOICE_HOST'

PRIVATE_KEY = '/SWM/Auth/PrivateCertificate'
PUBLIC_KEY = '/SWM/Auth/PublicCertificate'


def _get_ssm_value(ssm, key: str, decript: bool):
    parameter = ssm.get_parameter(Name=key, WithDecryption=decript)
    return parameter.get('Parameter', {}).get('Value')


def generate_jwt_token(field, value):
    code = OTPFacade.generate_code()

    ssm = boto3.client('ssm')
    private_key = _get_ssm_value(ssm, PRIVATE_KEY, True)
    public_key = _get_ssm_value(ssm, PUBLIC_KEY, True)

    jwt = JWT(
        private_key=private_key.encode(),
        public_key=public_key.encode()
    )

    session = SessionBuilder()\
        .with_type(SessionType.OTP_REQUEST)\
        .with_data({
            field: value,
            'otp_hash': code.hex_
        })\
        .build()

    jwt_token = jwt.encode(
        **session.to_dict(),
        expired=(datetime.now() + timedelta(minutes=30)).timestamp(),
    )

    return code, jwt_token


def get_key_value_param(event):
    body = get_json_body(event)
    if not body:
        raise RequestException("Request inválido!")

    cellphone = body.get("cellphone")
    email = body.get("email")
    if not cellphone and not email:
        raise RequestException("Informe o e-mail ou o telefone")

    field = 'email' if email else 'cellphone'
    value = email if email else cellphone
    return field, value


@default_api_gw_handler
def handler(event, context):
    field, value = get_key_value_param(event)

    code, jwt_token = generate_jwt_token(field, value)

    headers = {
        'Set-Cookie': get_jwt_cookie_value(jwt_token)
    }

    if 'true' != os.getenv(SEND_SMS_DISABLED, 'false').lower():
        user = UserFacade.get_user(field, value)
        if user:
            cellphone = user.cellphone

            client = Cliente(access_token=os.getenv(TOTALVOICE_TOKEN), host=os.getenv(TOTALVOICE_HOST))
            client.sms.enviar(cellphone, f'Código para acessar o StartupWeekend {code.code}')

    return buid_default_response(
        status=200,
        body=json.dumps(
            {
                'message': 'Um código de verificação de identidade foi enviado para o seu telefone '
                           'caso o telefone ou e-mail informado esteja cadastrado'
            },
            cls=SWMJSONEncoder
        ),
        headers=headers
    )


if __name__ == '__main__':
    handler({'body': '{"cellphone": "47992181825"}'}, None)
