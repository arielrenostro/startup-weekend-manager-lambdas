from swm.business import authentication as AuthenticationBusiness


def handler(event, context):
    headers = {}

    AuthenticationBusiness.define_cors_headers(event, headers)

    return {
        'statusCode': 200,
        'headers': headers,
        'body': ''
    }


if __name__ == '__main__':
    print(handler({}, None))
