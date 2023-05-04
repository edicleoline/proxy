from framework.models.middlewareparam import MiddlewareParamModel
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from db import connection

@dataclass_json
@dataclass
class ModemMiddlewareParamModel(MiddlewareParamModel):
    value: str

    def __init__(self, id: int = None, middleware_id: int = None, name: str = None, name_translate: str = None, type: str = None, required: bool = True, created_at=None):                
        super().__init__(id, middleware_id, name, name_translate, type, required, created_at)                
        self.modem_id: int = None
        self.value = None

    @property
    def value(self):
        conn = connection()
        row = conn.execute("SELECT value FROM modem_middleware_param WHERE modem_id=? AND middleware_param_id=?", (self.modem_id, self.id)).fetchone()
        conn.close(True)

        if row == None:
            return None

        return row[0]

    @classmethod
    def find_by_middleware_id(cls, middleware_id, modem_id):
        params = super(ModemMiddlewareParamModel, cls).find_by_middleware_id(middleware_id)
        if params:
            for param in params: param.modem_id = modem_id
        return params
    
    def save_to_db(self):
        # super().save_to_db()

        conn = connection()

        conn.execute("DELETE FROM modem_middleware_param WHERE modem_id = ? AND middleware_param_id = ?", (self.modem_id, self.id))

        conn.execute("INSERT INTO modem_middleware_param (modem_id, middleware_param_id, value) VALUES (?, ?, ?)", (
            self.modem_id, self.id, self.value
            ))
        self.id = conn.last_insert_rowid()

        conn.close(True)