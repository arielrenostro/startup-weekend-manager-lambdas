from swm.exception.business_exception import BusinessException
from swm.model.pitch import Pitch
from swm.model.session import Session
from swm.model.user import User


def create_pitch(pitch: Pitch, pitch_by_name: Pitch, user: User):
    if not user:
        raise BusinessException('Usuário não encontrado para realizar o cadastro do Pitch')
    if pitch.votes:
        raise BusinessException('Não é permitido informar os votos no cadastro do Pitch')
    if pitch.approved:
        raise BusinessException('Não é permitido informar a aprovação no cadastro do Pitch')
    if not pitch.name:
        raise BusinessException('É obrigatório informar o nome da ideia no cadastro do Pitch')
    if pitch_by_name:
        raise BusinessException('Já existe um Pitch com este nome de ideia')

    pitch.user = user
    pitch.votes = 0
    pitch.approved = False


def vote_pitch(pitch: Pitch, session: Session):
    if not pitch:
        raise BusinessException('Pitch não encontrado!')

    user = session.real_user
    if not user.available_votes or user.available_votes <= 0:
        raise BusinessException('Usuário sem votos disponíveis!')

    user.available_votes -= 1
    pitch.votes += 1
