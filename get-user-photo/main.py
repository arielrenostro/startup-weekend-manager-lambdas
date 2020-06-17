import json

from swm.api_gateway_utils import buid_default_response, get_path_params
from swm.exception.request_exception import RequestException
from swm.facade import session as SessionFacade
from swm.facade import userphoto as UserPhotoFacade
from swm.swm_json_encoder import SWMJSONEncoder
from swm.wrapper.default_api_gw_handler import default_api_gw_handler


@default_api_gw_handler
def handler(event, context):
    path_params = get_path_params(event)
    oid = path_params.get('oid', None)
    if not oid:
        print(json.dumps(path_params))
        raise RequestException("ID inválido")

    session = SessionFacade.get_session_from_event(event)

    user_photo = UserPhotoFacade.get_user_photo(session, oid)

    if user_photo:
        return buid_default_response(
            status=200,
            body=user_photo.data,
            headers={'Content-Type': 'image/jpeg'},
            base64encoded=True
        )
    else:
        return buid_default_response(
            status=404,
            body=json.dumps(
                {'message': 'Imagem não encontrada'},
                cls=SWMJSONEncoder
            )
        )


if __name__ == '__main__':
    print(
        handler(
            {
                'pathParameters': {
                    'oid': '008bfdcf-85a9-460a-8d41-49ea23936a9c'
                }
                ,
                'requestContext': {
                    'authorizer': {
                        'jwt_payload': '{"type": "LOGGED","user": {"oid": "008bfdcf-85a9-460a-8d41-49ea23936a9c","name": "Ariel","email": "arielrenostro@gmail.com","cellphone": "47992181824","created_at": 1585099807,"updated_at": 1586914329,"type": "ADMIN"},"data": {},"exp": 1588123554,"nbf": 1588112703}'
                    }
                }
            },
            None
        )
    )
