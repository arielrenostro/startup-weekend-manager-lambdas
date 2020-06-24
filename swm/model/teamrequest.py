from datetime import datetime


class TeamRequestStatus:
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"

    values = [PENDING, REJECTED, APPROVED]


class TeamRequest:
    oid: str
    oid_user: str
    oid_team: str
    status: str
    created_at: datetime
    updated_at: datetime

    def __init__(self):
        self.oid = None
        self.oid_user = None
        self.oid_team = None
        self.status = None
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        return {
            'oid': self.oid,
            'oid_user': self.oid_user,
            'oid_team': self.oid_team,
            'status': self.status,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
        }


class TeamRequestBuilder:
    _oid: str
    _oid_user: str
    _oid_team: str
    _status: str
    _created_at: datetime
    _updated_at: datetime

    def __init__(self):
        self._oid = None
        self._oid_user = None
        self._oid_team = None
        self._status = None
        self._created_at = None
        self._updated_at = None

    def build(self):
        team_request = TeamRequest()
        team_request.oid = self._oid
        team_request.oid_user = self._oid_user
        team_request.oid_team = self._oid_team
        team_request.status = self._status
        team_request.created_at = self._created_at
        team_request.updated_at = self._updated_at
        return team_request

    def with_oid(self, oid: str):
        self._oid = oid
        return self

    def with_oid_user(self, oid_user: str):
        self._oid_user = oid_user
        return self

    def with_oid_team(self, oid_team):
        self._oid_team = oid_team
        return self

    def with_status(self, status):
        self._status = status
        return self

    def with_created_at(self, created_at):
        self._created_at = created_at
        return self

    def with_updated_at(self, updated_at):
        self._updated_at = updated_at
        return self

    def from_json(self, json):
        self.with_oid(json.get('oid'))
        self.with_oid_user(json.get('oid_user'))
        self.with_oid_team(json.get('oid_team'))
        self.with_status(json.get('status'))

        created_at = json.get('created_at')
        if created_at:
            created_at = datetime.fromtimestamp(created_at)
        self.with_created_at(created_at)

        updated_at = json.get('updated_at')
        if updated_at:
            updated_at = datetime.fromtimestamp(updated_at)
        self.with_updated_at(updated_at)
        return self
