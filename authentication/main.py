from http import cookies

import boto3
from jwt_rsa.token import JWT

from authentication.aws_auth_policy import AuthPolicy
from utils.api_gateway import get_headers

PRINCIPAL_ID_KEY = '/SWM/Auth/PrincipalID'
PRIVATE_KEY = '/SWM/Auth/PrivateCertificate'
PUBLIC_KEY = '/SWM/Auth/PublicCertificate'


def _get_ssm_value(ssm, key: str, decript: bool):
    parameter = ssm.get_parameter(Name=key, WithDecryption=decript)
    return parameter.get('Parameter', {}).get('Value')


def _get_jwt_encoded(event) -> str:
    headers = get_headers(event)
    if not headers:
        raise Exception('Headers not found')

    cookie = cookies.SimpleCookie()
    cookie.load(
        headers.get('Cookie', '')
    )

    jwt = cookie.get('jwt')
    if jwt:
        return jwt.value.encode()


def handler(event, context):
    jwt_encoded = _get_jwt_encoded(event)
    if not jwt_encoded:
        raise Exception('JWT not found')

    ssm = boto3.client('ssm')

    private_key = _get_ssm_value(ssm, PRIVATE_KEY, True)
    public_key = _get_ssm_value(ssm, PUBLIC_KEY, True)

    jwt = JWT(
        private_key=private_key.encode(),
        public_key=public_key.encode()
    )

    principal_id = _get_ssm_value(ssm, PRINCIPAL_ID_KEY, True)

    # If decode's ok, allow access
    jwt.decode(
        jwt_encoded,
        options={
            'require_exp': True,
            'verify_exp': True
        }
    )

    tmp = event['methodArn'].split(':')
    api_gateway_arn_tmp = tmp[5].split('/')
    aws_account_id = tmp[4]

    policy = AuthPolicy(principal_id, aws_account_id)
    policy.restApiId = api_gateway_arn_tmp[0]
    policy.region = tmp[3]
    policy.stage = api_gateway_arn_tmp[1]
    policy.allowAllMethods()

    # policy['context'] = {
    #     'jwt': ''
    # }

    return policy.build()


if __name__ == '__main__':
    handler(
        {
            'headers': {
                'Cookie': 'jwt=nanoisdnoiansodi'
            }
        },
        None
    )
