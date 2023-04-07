from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime
from marshmallow import fields

@dataclass_json
@dataclass
class ModemsAutoRotateAgendaItem():
    added_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )
    run_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )
    now: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )
    time_left_to_run: int

    def __init__(self, modem_state, added_at, run_at, now = None): 
        self.modem_state = modem_state       
        self.added_at = added_at
        self.run_at = run_at
        self.now = now
        self.time_left_to_run = None

    def ready_to_run(self):
        self.now = datetime.now()
        self.time_left_to_run = int((self.run_at - self.now).total_seconds())
        return True if self.time_left_to_run <= 0 else False