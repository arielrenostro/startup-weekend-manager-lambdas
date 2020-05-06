import json
import traceback
from datetime import datetime, timedelta
from http import cookies

import boto3
from jwt_rsa.token import JWT

from authentication.aws_auth_policy import AuthPolicy
from swm.api_gateway_utils import get_headers
from swm.business import authentication as AuthenticationBusiness
from swm.exception.business_exception import BusinessException
from swm.model.session import SessionBuilder

PRINCIPAL_ID_KEY = '/SWM/Auth/PrincipalID'
PRIVATE_KEY = '/SWM/Auth/PrivateCertificate'
PUBLIC_KEY = '/SWM/Auth/PublicCertificate'
BEARER_LENGTH = len("Bearer")


def _get_ssm_value(ssm, key: str, decript: bool):
    parameter = ssm.get_parameter(Name=key, WithDecryption=decript)
    return parameter.get('Parameter', {}).get('Value')


def _get_jwt_encoded(event) -> str:
    headers = get_headers(event)
    if not headers:
        raise Exception('Headers not found')

    jwt = _get_jwt_by_header(headers)
    if not jwt:
        jwt = _get_jwt_by_cookie(headers)

    if jwt:
        return jwt.encode()


def _get_jwt_by_header(headers):
    authorization = headers.get('Authorization')
    if authorization:
        return authorization[BEARER_LENGTH + 1:]  # +1 = space


def _get_jwt_by_cookie(headers):
    cookie = cookies.SimpleCookie()
    cookie.load(
        headers.get('Cookie', '')
    )
    jwt = cookie.get('jwt')
    if jwt:
        return jwt.value


def _create_jwt(ssm):
    private_key = _get_ssm_value(ssm, PRIVATE_KEY, True)
    public_key = _get_ssm_value(ssm, PUBLIC_KEY, True)
    return JWT(
        private_key=private_key.encode(),
        public_key=public_key.encode()
    )


def _create_policy_base(event, ssm):
    principal_id = _get_ssm_value(ssm, PRINCIPAL_ID_KEY, True)

    tmp = event['methodArn'].split(':')

    api_gateway_arn_tmp = tmp[5].split('/')
    aws_account_id = tmp[4]

    policy = AuthPolicy(principal_id, aws_account_id)
    policy.restApiId = api_gateway_arn_tmp[0]
    policy.region = tmp[3]
    policy.stage = api_gateway_arn_tmp[1]

    return policy


def _populate_policy_context(decoded, jwt, policy):
    if decoded:
        policy.context = {
            'jwt_payload': json.dumps(decoded),
            'jwt': jwt.encode(
                **decoded,
                expired=(datetime.now() + timedelta(hours=3)).timestamp(),
            )
        }
        print(policy.context)


def handler(event, context):
    jwt_encoded = _get_jwt_encoded(event)

    ssm = boto3.client('ssm')
    policy = _create_policy_base(event, ssm)

    try:
        jwt = None
        decoded = None
        session = None

        if jwt_encoded:
            jwt = _create_jwt(ssm)
            try:
                # If decode's ok, allow access
                decoded = jwt.decode(
                    jwt_encoded,
                    options={
                        'require_exp': True,
                        'verify_exp': True
                    }
                )
                session = SessionBuilder().from_json(decoded).build()
            except Exception as e:
                AuthenticationBusiness.validate_jwt_fail(event, e)

        AuthenticationBusiness.validate_authentication(event, session)

        policy.allowAllMethods()
        _populate_policy_context(decoded, jwt, policy)

        if decoded:
            print(f'Allowed to {decoded.get("oid")} - {decoded.get("name")}')
        else:
            print(f'Allowed to anonymous')

    except BusinessException as e:
        policy.denyAllMethods()
        print(f'Denied because "{e.message}"')

    except Exception as e:
        policy.denyAllMethods()
        print(f'Denied to {jwt_encoded}')
        traceback.print_exc()

    return policy.build()


if __name__ == '__main__':
    # print('testebatatao'[4:])
    handler(
        {
            'headers': {
                'Cookie': 'jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJlbWFpbCI6ImFyaWVscmVub3N0cm9AZ21haWwuY29tMTEiLCJvdHBfaGFzaCI6IjMwYzYwNWE0LTI4NTAtNGQ0Yy1hYjJlLWJkMjlmNWFkOTE3NSIsImV4cCI6MTU4NTY5ODM3NCwibmJmIjoxNTg1Njk2NTU0fQ.GB4fKOsjW-vGX9i6xiFXgKO25U8gNTDBNjXvAASecHVftXItloehTz_JUAsYicrWM-OTWqijNKgUYzLb1_BRjJbfY1z7CWOxivlN5qKIthcFSdixRmIdIFVA-rq-XGsfG5CG6R-IBFBKVjRtDedOjm-HQqlDqAgQaJFj8IhiLYyou6st3NQk4i8xRL2dxPrDBdgpRDAOl4H4Hy7PBbMMXvL-cQycYyHEVUKrTDn6c60c0983-YqkOwUl1U6x1pZFkpAXcj_ElRF51UmpvR01MRCcKJm8BrEZzrw4chPUaqcr8-6yFbkNpeWZm9mFof0YI6-hnFm5pgeT32wTEm8aXg'
            }
        },
        None
    )
