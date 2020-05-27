from datetime import datetime

from swm.model.user import User


class PitchVote:
    oid_user: str
    date: datetime

    def to_dict(self):
        return {
            'oid_user': self.oid_user,
            'date': int(self.date.timestamp()) if self.date else None,
        }


class Pitch:
    oid: str
    name: str
    user: User
    created_at: datetime
    updated_at: datetime
    votes: []
    approved: bool

    def to_dict(self):
        return {
            'oid': self.oid,
            'name': self.name,
            'oid_user': self.user.oid if self.user else None,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
            'votes': [v.to_dict() for v in self.votes],
            'approved': self.approved
        }


class PitchBuilder:
    _oid: str
    _name: str
    _user: User
    _created_at: datetime
    _updated_at: datetime
    _votes: []
    _approved: bool

    def __init__(self):
        self._oid = None
        self._name = None
        self._user = None
        self._created_at = None
        self._updated_at = None
        self._votes = []
        self._approved = None

    def build(self) -> Pitch:
        pitch = Pitch()
        pitch.oid = self._oid
        pitch.name = self._name
        pitch.user = self._user
        pitch.created_at = self._created_at
        pitch.updated_at = self._updated_at
        pitch.votes = self._votes
        pitch.approved = self._approved
        return pitch

    def with_oid(self, oid):
        self._oid = oid
        return self

    def with_name(self, name):
        self._name = name
        return self

    def with_user(self, user):
        self._user = user
        return self

    def with_created_at(self, created_at):
        self._created_at = created_at
        return self

    def with_updated_at(self, updated_at):
        self._updated_at = updated_at
        return self

    def with_votes(self, votes):
        if votes:
            pitch_votes = []
            for vote in votes:
                pich_vote = PitchVote()
                pich_vote.oid_user = vote['oid_user']
                pich_vote.date = datetime.fromtimestamp(vote['date'])
                pitch_votes.append(pich_vote)
            self._votes = pitch_votes
        return self

    def with_approved(self, approved):
        self._approved = approved
        return self

    def from_json(self, item):
        self.with_oid(item.get('oid'))
        self.with_name(item.get('name'))
        self.with_user(item.get('user'))
        self.with_votes(item.get('votes'))
        self.with_approved(item.get('approved'))

        created_at = item.get('created_at')
        if created_at:
            created_at = datetime.fromtimestamp(created_at)
        self.with_created_at(created_at)

        updated_at = item.get('updated_at')
        if updated_at:
            updated_at = datetime.fromtimestamp(updated_at)
        self.with_updated_at(updated_at)

        return self
