import decimal
import json

from swm.model.user import User


class SWMJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, User):
            return o.to_json_str()
        return super(SWMJSONEncoder, self).default(o)
