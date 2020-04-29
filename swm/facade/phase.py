import os
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr

from swm.business import phase as PhaseBusiness
from swm.model.phase import Phase, PhaseBuilder

TABLE_ENV = 'PHASE_TABLE'
TABLE_ENV_DEFAULT = 'SWM_PHASE'


def save(phase: Phase):
    table = _get_table()

    if not phase.oid:
        phase.oid = str(uuid4())

    table.put_item(Item=phase.to_dict())


def get_current_phase() -> Phase:
    table = _get_table()
    query = table.scan(
        FilterExpression=Attr('selected').eq(True)
    )

    items = query['Items']
    if len(items) > 0:
        item = items[0]
        return PhaseBuilder().from_json(item).build()


def list_phases() -> Phase:
    return PhaseBusiness.list_phases()


def select_phase_by_name(phase_name):
    def _current_phase_provider():
        return get_current_phase()

    old_phase, new_phase = PhaseBusiness.select_phase_by_name(phase_name, _current_phase_provider)

    if old_phase:
        save(old_phase)
    save(new_phase)

    return old_phase, new_phase


def _get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.getenv(TABLE_ENV, TABLE_ENV_DEFAULT))
