import decimal
import json

from swm.model.pitch import Pitch, PitchVote
from swm.model.session import Session
from swm.model.user import User


class SWMJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)

        elif isinstance(o, User):
            return o.to_dict()

        elif isinstance(o, Session):
            return o.to_dict()

        elif isinstance(o, Pitch):
            return o.to_dict()

        elif isinstance(o, PitchVote):
            return o.to_dict()

        return super(SWMJSONEncoder, self).default(o)
