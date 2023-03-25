from db import connection
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from enum import Enum
from datetime import datetime
from marshmallow import fields
import json

from framework.helper.database.pagination import PaginateDirection, PaginateOrder

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

    def __init__(self, id = None, modem_id = None, owner = None, type = None, message = None, code = None, params = None, logged_at = datetime.now(), created_at = None):
        self.id = id
        self.modem_id = modem_id
        self.owner = owner
        self.type = type
        self.message = message
        self.code = code
        self.params = params
        self.params_json = json.dumps(params) if params else None
        self.logged_at = logged_at
        self.created_at = created_at    

    @classmethod
    def paginate_by_id(cls, id, cursor = None, limit = 20, direction: PaginateDirection = PaginateDirection.NEXT, order: PaginateOrder = PaginateOrder.ASC):
        conn = connection()
        cursor_sql = None
        if cursor:
            cursor_sql = 'and id {0} {1}'.format(
                    ('>' if direction == PaginateDirection.NEXT else '<'),
                    cursor
                )
        else:
            cursor_sql = ''

        rows = conn.execute("""
                select id, modem_id, owner, type, message, code, params_json, logged_at 
                    from modem_log 
                    where modem_id = {0} {1} 
                    order by id {2} 
                    limit {3}
            """.format(id, cursor_sql, order.value, limit)).fetchall()
        conn.close(True)

        items = []
        for row in rows:
            items.append(
                ModemLogModel(
                    id = row[0],
                    modem_id = row[1], 
                    owner = ModemLogOwner(row[2]), 
                    type = ModemLogType(row[3]), 
                    message = row[4],
                    code = row[5],
                    params = json.loads(row[6]) if row[6] else None,
                    logged_at = datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S')
                )
            )

        return items

        

    def save_to_db(self):
        conn = connection()
        conn.execute("insert into modem_log (modem_id, owner, type, message, code, params_json, logged_at) values (?, ?, ?, ?, ?, ?, ?)", (
            self.modem_id, self.owner.value, self.type.value, self.message, self.code, self.params_json, self.logged_at.strftime("%Y-%m-%d %H:%M:%S")
            ))
        self.id = conn.last_insert_rowid()
        conn.close(True)