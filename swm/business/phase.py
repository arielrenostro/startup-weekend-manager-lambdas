from datetime import datetime

from swm.exception.business_exception import BusinessException
from swm.model.phase import PhaseBuilder, Phase

NOT_STARTED = 'NOT_STARTED'
OPENING = 'OPENING'
PITCH_TIME = 'PITCH_TIME'
VOTE_PITCH = 'VOTE_PITCH'
ASSEMBLING_TEAMS = 'ASSEMBLING_TEAMS'
WORK_HARD = 'WORK_HARD'
JUDGES_VOTE = 'JUDGES_VOTE'
FINISHED = 'FINISHED'

PHASES = [
    PhaseBuilder().with_name(NOT_STARTED).with_description('Não iniciado').build(),
    PhaseBuilder().with_name(OPENING).with_description('Abertura do evento').build(),
    PhaseBuilder().with_name(PITCH_TIME).with_description('Pitch Time').build(),
    PhaseBuilder().with_name(VOTE_PITCH).with_description('Votação dos pitch\'s').build(),
    PhaseBuilder().with_name(ASSEMBLING_TEAMS).with_description('Montagem das equipes').build(),
    PhaseBuilder().with_name(WORK_HARD).with_description('Work hard').build(),
    PhaseBuilder().with_name(JUDGES_VOTE).with_description('Votação dos juízes').build(),
    PhaseBuilder().with_name(FINISHED).with_description('Finalizado').build(),
]


def list_phases(simple=True):
    if simple:
        return [{'name': p.name, 'description': p.description} for p in PHASES]
    return PHASES


def get_phase_by_name(phase_name) -> Phase:
    for phase in PHASES:
        if phase_name == phase.name:
            return phase
    raise BusinessException(f'Fase {phase_name} não encontrada')


def select_phase_by_name(phase_name, current_phase_provider) -> (Phase, Phase):
    if not phase_name:
        raise BusinessException('Nome da fase não informada!')

    phase: Phase = get_phase_by_name(phase_name)
    current_phase: Phase = current_phase_provider()

    if current_phase:
        current_phase.selected = False
        current_phase.deselected_at = datetime.now()

    phase.selected = True
    phase.selected_at = datetime.now()

    return current_phase, phase


def is_vote_pitch(current_phase: Phase):
    return current_phase.name == VOTE_PITCH
