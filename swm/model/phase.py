from datetime import datetime


class Phase:
    oid: str
    name: str
    description: str
    selected: bool
    selected_at: datetime
    deselected_at: datetime

    def to_dict(self):
        return {
            'oid': self.oid,
            'name': self.name,
            'description': self.description,
            'selected': self.selected,
            'selected_at': int(self.selected_at.timestamp()) if self.selected_at else None,
            'deselected_at': int(self.deselected_at.timestamp()) if self.deselected_at else None,
        }


class PhaseBuilder:
    _oid: str
    _name: str
    _description: str
    _selected: bool
    _selected_at: datetime
    _deselected_at: datetime

    def __init__(self):
        self._oid = None
        self._name = None
        self._description = None
        self._selected = None
        self._selected_at = None
        self._deselected_at = None

    def build(self):
        phase = Phase()
        phase.oid = self._oid
        phase.name = self._name
        phase.description = self._description
        phase.selected = self._selected
        phase.selected_at = self._selected_at
        phase.deselected_at = self._deselected_at
        return phase

    def with_oid(self, oid: str):
        self._oid = oid
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_description(self, description: str):
        self._description = description
        return self

    def with_selected(self, selected: bool):
        self._selected = selected
        return self

    def with_selected_at(self, selected_at: datetime):
        self._selected_at = selected_at
        return self

    def with_deselected_at(self, deselected_at: datetime):
        self._deselected_at = deselected_at
        return self

    def from_json(self, json):
        self.with_oid(json.get('oid'))
        self.with_name(json.get('name'))
        self.with_description(json.get('description'))
        self.with_selected(json.get('selected'))

        selected_at = json.get('selected_at')
        if selected_at:
            self.with_selected_at(datetime.fromtimestamp(selected_at))

        deselected_at = json.get('deselected_at')
        if deselected_at:
            self.with_deselected_at(datetime.fromtimestamp(deselected_at))

        return self