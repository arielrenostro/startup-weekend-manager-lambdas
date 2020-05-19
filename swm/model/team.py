from datetime import datetime
from typing import List

from swm.model.user import User


class TempUser:
    oid: str

    def __init__(self, oid):
        self.oid = oid


class Team:
    oid: str
    name: str
    leader: User
    members: List[User]
    created_at: datetime
    updated_at: datetime

    def __init__(self):
        self.oid = None
        self.name = None
        self.leader = None
        self.members = []
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        return {
            'oid': self.oid,
            'name': self.name,
            'oid_leader': self.leader.oid if self.leader else None,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
            'members': [m.oid for m in self.members]
        }


class TeamBuilder:
    _oid: str
    _name: str
    _leader: User
    _members: List[User]
    _created_at: datetime
    _updated_at: datetime

    def __init__(self):
        self._oid = None
        self._name = None
        self._leader = None
        self._members = None
        self._created_at = None
        self._updated_at = None

    def build(self):
        team = Team()
        team.oid = self._oid
        team.name = self._name
        team.leader = self._leader
        team.members = self._members
        team.created_at = self._created_at
        team.updated_at = self._updated_at
        return team

    def with_oid(self, oid: str):
        self._oid = oid
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_oid_leader(self, oid_leader):
        if oid_leader:
            self._leader = TempUser(oid_leader)
        return self

    def with_leader(self, leader: User):
        if leader:
            self._leader = leader
        return self

    def with_members(self, members):
        if len(members) > 0 and isinstance(members[0], str):
            self._members = [TempUser(oid) for oid in members]
        else:
            self._members = members
        return self

    def with_created_at(self, created_at):
        self._created_at = created_at
        return self

    def with_updated_at(self, updated_at):
        self._updated_at = updated_at
        return self

    def from_json(self, json):
        self.with_oid(json.get('oid'))
        self.with_name(json.get('name'))
        self.with_oid_leader(json.get('oid_leader'))
        self.with_leader(json.get('leader'))
        self.with_members(json.get('members'))

        created_at = json.get('created_at')
        if created_at:
            created_at = datetime.fromtimestamp(created_at)
        self.with_created_at(created_at)

        updated_at = json.get('updated_at')
        if updated_at:
            updated_at = datetime.fromtimestamp(updated_at)
        self.with_updated_at(updated_at)
        return self
