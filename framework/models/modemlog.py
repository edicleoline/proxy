from db import connection
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from enum import Enum
from datetime import datetime
from marshmallow import fields
import json

class ModemLogOwnerField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        return ModemLogOwner[value]
    
modem_log_owner_field = {
    "dataclasses_json": {
        "encoder": lambda owner: owner.name,
        "decoder": lambda name: ModemLogOwner(name),
        "mm_field": ModemLogOwnerField(),
    }
}

class ModemLogTypeField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        return ModemLogTypeField[value]
    
modem_log_type_field = {
    "dataclasses_json": {
        "encoder": lambda type: type.name,
        "decoder": lambda name: ModemLogTypeField(name),
        "mm_field": ModemLogTypeField(),
    }
}
    
class ModemLogOwner(Enum):
    SYSTEM  = 1
    USER    = 2

class ModemLogType(Enum):
    SUCCESS    = 0
    INFO       = 1
    WARNING    = 2
    ERROR      = 3

@dataclass_json
@dataclass
class ModemLogModel():
    id: int
    modem_id: int
    owner: ModemLogOwner = field(metadata=modem_log_owner_field)
    type: ModemLogType = field(metadata=modem_log_type_field)
    message: str
    code: str
    params: object
    logged_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )

    def __init__(self, modem_id = None, owner = None, type = None, message = None, code = None, params = None, logged_at = datetime.now(), created_at = None):
        self.modem_id = modem_id
        self.owner = owner
        self.type = type
        self.message = message
        self.code = code
        self.params = params
        self.params_json = json.dumps(params) if params else None
        self.logged_at = logged_at
        self.created_at = created_at    
    
    def json(self):
        return {
            'id': self.id,
            'owner': self.owner.name,
            'type': self.type.name,
            'message': self.message,
            'code': self.code,
            'params_json': self.params_json,
            'logged_at': self.logged_at
        }        

    def save_to_db(self):
        conn = connection()
        conn.execute("insert into modem_log (modem_id, owner, type, message, code, params_json, logged_at) values (?, ?, ?, ?, ?, ?, ?)", (
            self.modem_id, self.owner.value, self.type.value, self.message, self.code, self.params_json, self.logged_at.strftime("%Y-%m-%d %H:%M:%S")
            ))
        self.id = conn.last_insert_rowid()
        conn.close(True)