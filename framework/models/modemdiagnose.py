from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from enum import Enum
from datetime import datetime
from marshmallow import fields
import json
import uuid

class ModemDiagnoseOwnerField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        return ModemDiagnoseOwner[value]
    
modem_diagnose_owner_field = {
    "dataclasses_json": {
        "encoder": lambda owner: owner.name,
        "decoder": lambda name: ModemDiagnoseOwner(name),
        "mm_field": ModemDiagnoseOwnerField(),
    }
}

class ModemDiagnoseTypeField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        return ModemDiagnoseTypeField[value]
    
modem_diagnose_type_field = {
    "dataclasses_json": {
        "encoder": lambda type: type.name,
        "decoder": lambda name: ModemDiagnoseTypeField(name),
        "mm_field": ModemDiagnoseTypeField(),
    }
}
    
class ModemDiagnoseOwner(Enum):
    SYSTEM    = 1
    USER      = 2

class ModemDiagnoseType(Enum):
    SUCCESS    = 0
    INFO       = 1
    WARNING    = 2
    ERROR      = 3

@dataclass_json
@dataclass
class ModemDiagnoseModel():
    id: str
    modem_id: int
    owner: ModemDiagnoseOwner = field(metadata=modem_diagnose_owner_field)
    type: ModemDiagnoseType = field(metadata=modem_diagnose_type_field)
    message: str
    code: str
    params: object
    description: str
    require_answer: bool
    logged_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )

    def __init__(
            self, 
            id = None, 
            modem_id = None, 
            owner = None, 
            type = None, 
            message = None, 
            code = None, 
            params = None, 
            description = None,
            require_answer = False,
            logged_at = datetime.now(),             
            created_at = None
    ):
        self.id = self.generate_id() if id == None else id
        self.modem_id = modem_id
        self.owner = owner
        self.type = type
        self.message = message
        self.code = code
        self.params = params
        self.description = description
        self.require_answer = require_answer
        self.logged_at = logged_at
        self.created_at = created_at    

    def generate_id(self):
        return uuid.uuid4()