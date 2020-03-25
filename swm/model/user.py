import hashlib
import json
from datetime import datetime


class User:
    oid: str
    name: str
    email: str
    cellphone: str
    password: str
    created_at: datetime
    updated_at: datetime

    def to_json_str(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {
            'oid': self.oid,
            'name': self.name,
            'email': self.email,
            'cellphone': self.cellphone,
            'password': self.password,
            'created_at': self.created_at.timestamp() if self.created_at else None,
            'updated_at': self.updated_at.timestamp() if self.updated_at else None
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
        if encrypt:
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

    def from_json(self, item):
        self.with_oid(item.get('oid'))
        self.with_name(item.get('name'))
        self.with_email(item.get('email'))
        self.with_cellphone(item.get('cellphone'))
        self.with_password(item.get('password'), encrypt=False)

        created_at = item.get('created_at')
        if created_at:
            created_at = datetime.fromtimestamp(created_at)
        self.with_created_at(created_at)

        updated_at = item.get('updated_at')
        if updated_at:
            updated_at = datetime.fromtimestamp(updated_at)
        self.with_updated_at(updated_at)

        return self
