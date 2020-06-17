from datetime import datetime


class UserPhoto:
    oid_user: str
    data: str
    created_at: datetime
    updated_at: datetime

    def __init__(self):
        self.oid_user = None
        self.data = None
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        return {
            'oid_user': self.oid_user,
            'data': self.data,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
        }


class UserPhotoBuilder:
    oid_user: str
    data: str
    created_at: datetime
    updated_at: datetime

    def __init__(self):
        self.oid_user = None
        self.data = None
        self.created_at = None
        self.updated_at = None

    def with_oid_user(self, oid_user):
        self.oid_user = oid_user
        return self

    def with_data(self, data):
        self.data = data
        return self

    def with_created_at(self, created_at):
        self.created_at = created_at
        return self

    def with_updated_at(self, updated_at):
        self.updated_at = updated_at
        return self

    def from_json(self, json: dict):
        self.with_oid_user(json.get('oid_user'))
        self.with_data(json.get('data'))
        created_at = json.get('created_at')
        if created_at:
            created_at = datetime.fromtimestamp(created_at)
        self.with_created_at(created_at)

        updated_at = json.get('updated_at')
        if updated_at:
            updated_at = datetime.fromtimestamp(updated_at)
        self.with_updated_at(updated_at)
        return self

    def build(self) -> UserPhoto:
        user_photo = UserPhoto()
        user_photo.data = self.data
        user_photo.oid_user = self.oid_user
        user_photo.created_at = self.created_at
        user_photo.updated_at = self.updated_at
        return user_photo
