from datetime import datetime

from swm.model.user import User, UserBuilder


class SessionType:
    OTP_REQUEST = 'OTP_REQUEST'
    LOGGED = 'LOGGED'


class UserSession:
    oid: str
    name: str
    email: str
    cellphone: str
    created_at: datetime
    updated_at: datetime
    type_: str

    def __init__(self, user):
        self.oid = user.oid
        self.name = user.name
        self.email = user.email
        self.cellphone = user.cellphone
        self.created_at = user.created_at
        self.updated_at = user.updated_at
        self.type_ = user.type_

    def to_dict(self):
        return {
            'oid': self.oid,
            'name': self.name,
            'email': self.email,
            'cellphone': self.cellphone,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
            'type': self.type_
        }


class Session:
    type_: str
    user: UserSession
    data: dict

    def __init__(self):
        self.type_ = None
        self.user = None
        self.data = {}

    def to_dict(self):
        return {
            'type': self.type_,
            'user': self.user.to_dict() if self.user else None,
            'data': self.data
        }


class SessionBuilder:
    _session: Session

    def __init__(self):
        self._session = Session()

    def build(self):
        return self._session

    def with_user(self, user: User):
        self._session.user = UserSession(user)
        return self

    def with_type(self, type_):
        self._session.type_ = type_
        return self

    def with_data(self, data):
        if data:
            self._session.data = data
        return self

    def from_json(self, item):
        self.with_type(item.get('type'))
        self.with_data(item.get('data'))

        user_json = item.get('user')
        if user_json:
            user = UserBuilder().from_json(user_json).build()
            self.with_user(user)

        return self
