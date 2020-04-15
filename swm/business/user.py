from swm.exception.request_exception import RequestException


def create_user(user, user_by_cellphone, user_by_email):
    if user_by_email or user_by_cellphone:
        raise RequestException('Já existe um usuário com o mesmo telefone ou e-mail')
    if user.oid:
        raise RequestException("OID deve ser gerado dinamicamente")
    if not user.password:
        raise RequestException("Campo 'password' é obrigatório")
    if not user.cellphone:
        raise RequestException("Campo 'cellphone' é obrigatório")

    user.available_votes = 5
