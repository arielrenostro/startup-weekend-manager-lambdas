from swm.api_gateway_utils import get_jwt_payload
from swm.model.session import Session, SessionBuilder
from swm.model.user import User


def get_session_from_event(event) -> Session:
    payload = get_jwt_payload(event)
    session = SessionBuilder().from_json(payload).build()
    _populate_updated_user(session)
    return session


def _populate_updated_user(session: Session) -> None:
    session.real_user = _get_user(session.user.oid)


def _get_user(oid_user) -> User:
    if oid_user:
        from swm.facade import user as UserFacade
        return UserFacade.get_user_by_oid(oid_user)
