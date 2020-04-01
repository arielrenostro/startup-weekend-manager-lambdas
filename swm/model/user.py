import hashlib
from datetime import datetime


class UserType:
    NORMAL = 'NORMAL'
    ADMIN = 'ADMIN'

    VALUES = {
        NORMAL,
        ADMIN
    }


class User:
    oid: str
    name: str
    email: str
    cellphone: str
    password: str
    created_at: datetime
    updated_at: datetime
    type_: str

    def to_dict(self):
        return {
            'oid': self.oid,
            'name': self.name,
            'email': self.email,
            'cellphone': self.cellphone,
            'password': self.password,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
            'type': self.type_
        }


class UserBuilder:
    _user: User

    def __init__(self):
        self._user = User()

    def build(self):
        return self._user

    def with_oid(self, oid: str):
        self._user.oid = oid
        return self

    def with_name(self, name: str):
        self._user.name = name
        return self

    def with_cellphone(self, cellphone: str):
        self._user.cellphone = cellphone
        return self

    def with_email(self, email: str):
        self._user.email = email
        return self

    def with_password(self, password: str, encrypt: bool = True):
        if encrypt and password:
            self._user.password = hashlib.sha256(password.encode()).hexdigest()
        else:
            self._user.password = password
        return self

    def with_created_at(self, created_at: datetime = None):
        if not created_at:
            created_at = datetime.now()
        self._user.created_at = created_at
        return self

    def with_updated_at(self, updated_at: datetime = None):
        if not updated_at:
            updated_at = datetime.now()
        self._user.updated_at = updated_at
        return self

    def with_type(self, type_: str):
        if type_ in UserType.VALUES:
            self._user.type_ = type_
        return self

    def from_json(self, item, encrypt_password=False):
        self.with_oid(item.get('oid'))
        self.with_name(item.get('name'))
        self.with_email(item.get('email'))
        self.with_cellphone(item.get('cellphone'))
        self.with_password(item.get('password'), encrypt=encrypt_password)
        self.with_type(item.get('type', UserType.NORMAL))

        created_at = item.get('created_at')
        if created_at:
            created_at = datetime.fromtimestamp(created_at)
        self.with_created_at(created_at)

        updated_at = item.get('updated_at')
        if updated_at:
            updated_at = datetime.fromtimestamp(updated_at)
        self.with_updated_at(updated_at)

        return self
