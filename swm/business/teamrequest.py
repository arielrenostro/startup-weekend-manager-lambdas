from swm.business import phase as PhaseBusiness
from swm.business import team as TeamBusiness
from swm.exception.business_exception import BusinessException
from swm.model.phase import Phase
from swm.model.teamrequest import TeamRequestStatus, TeamRequest
from swm.model.user import User


def validate_new_request(
        user: User,
        oid_team: str,
        current_phase: Phase,
        _get_requests_by_oid_user_provider,
        _get_team_provider
):
    if PhaseBusiness.ASSEMBLING_TEAMS != current_phase.name:
        raise BusinessException('Não é fase de montagem de equipes para poder solicitar entrada em algum time')

    if user.team is not None:
        raise BusinessException(f'Você já faz parte do time "{user.team.name}" e não é possível juntar-se a outro time')

    team = _get_team_provider(oid_team)
    if not team:
        raise BusinessException('Time não encontrado')

    requests = _get_requests_by_oid_user_provider(user.oid)
    for request in requests:
        if request.oid_team == oid_team and not TeamRequestStatus.REJECTED == request.status:
            raise BusinessException(f'Você já solicitou entrada a este time. Aguarde ela ser aprovada ou rejeitada')


def approve_request(team_request: TeamRequest, user: User, _get_user_provider, _get_team_provider):
    _validate_request(team_request, user)

    team = _get_team_provider(team_request.oid_team)

    if len(team.members) >= TeamBusiness.TEAMS_SIZE:
        raise BusinessException(f"O time já está cheio")

    user = _get_user_provider(team_request.oid_user)

    team_request.status = TeamRequestStatus.APPROVED

    user.team = team
    team.members.append(user)

    return user, team


def reject_request(team_request: TeamRequest, user: User):
    _validate_request(team_request, user)
    team_request.status = TeamRequestStatus.REJECTED


def _validate_request(team_request, user):
    if team_request is None:
        raise BusinessException("Solicitação não encontrada")

    if user.team.leader.oid != user.oid:
        raise BusinessException("Seu usuário não é um líder de equipe para poder aprovar uma solicitação")

    if user.team.oid != team_request.oid_team:
        raise BusinessException("A solicitação não é da sua equipe")

    if team_request.status != TeamRequestStatus.PENDING:
        msg = "Aprovada" if TeamRequestStatus.APPROVED == team_request.status else "Rejeitada"
        raise BusinessException(f'A solicitação já está com o status "{msg}"')
