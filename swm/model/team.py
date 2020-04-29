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

    def to_dict(self):
        return {
            'oid': self.oid,
            'name': self.name,
            'oid_leader': self.leader.oid if self.leader else None,
            'members': [m.oid for m in self.members]
        }


class TeamBuilder:
    _oid: str
    _name: str
    _leader: User
    _members: List[User]

    def __init__(self):
        self._oid = None
        self._name = None
        self._leader = None
        self._members = None

    def build(self):
        team = Team()
        team.oid = self._oid
        team.name = self._name
        team.leader = self._leader
        team.members = self._members
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
        self._leader = leader
        return self

    def with_members(self, members):
        if len(members) > 0 and isinstance(members[0], str):
            self._members = [TempUser(oid) for oid in members]
        else:
            self._members = members
        return self

    def from_json(self, json):
        self.with_oid(json.get('oid'))
        self.with_name(json.get('name'))
        self.with_oid_leader(json.get('oid_leader'))
        self.with_leader(json.get('leader'))
        self.with_members(json.get('members'))
        return self
