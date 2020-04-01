from swm.api_gateway_utils import get_jwt_payload
from swm.model.session import Session, SessionBuilder


def get_session_from_event(event) -> Session:
    payload = get_jwt_payload(event)
    return SessionBuilder().from_json(payload).build()
