import json
from datetime import datetime, timedelta

import boto3
from jwt_rsa.token import JWT

from swm.api_gateway_utils import buid_default_response
from swm.wrapper.default_api_gw_handler import default_api_gw_handler

PRIVATE_KEY = '/SWM/Auth/PrivateCertificate'
PUBLIC_KEY = '/SWM/Auth/PublicCertificate'


def _get_ssm_value(ssm, key: str, decript: bool):
    parameter = ssm.get_parameter(Name=key, WithDecryption=decript)
    return parameter.get('Parameter', {}).get('Value')


@default_api_gw_handler
def handler(event, context):
    ssm = boto3.client('ssm')

    private_key = _get_ssm_value(ssm, PRIVATE_KEY, True)
    public_key = _get_ssm_value(ssm, PUBLIC_KEY, True)

    jwt = JWT(
        private_key=private_key.encode(),
        public_key=public_key.encode()
    )
    token = jwt.encode(
        expired=(datetime.now() + timedelta(days=365)).timestamp(),
        oid=1,
        name='Ariel'
    )

    print(token)

    return buid_default_response(
        status=200,
        body=json.dumps({

        }),
        headers={
            'Set-Cookie': 'jwt=' + token + '; path=/'
        }
    )


handler(None, None)
