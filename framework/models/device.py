from db import connection
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from framework.models.middleware import MiddlewareModel

@dataclass_json
@dataclass
class DeviceModel():
    id: int
    model: str
    type: str  
    middleware: MiddlewareModel
    
    def __init__(self, id = None, model = None, type = None, middleware_id = None, created_at = None):
        self.id = id
        self.model = model
        self.type = type
        self.middleware_id = middleware_id
        self._middleware = None
        self.created_at = created_at        

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, model, type, middleware_id, created_at from device where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return DeviceModel(id = row[0], model = row[1], type = row[2], middleware_id = row[3], created_at = row[4])
    
    @classmethod
    def all(cls):
        conn = connection()
        rows = conn.execute("select id from device order by id asc").fetchall()
        conn.close(True)

        devices = []
        for row in rows:
            devices.append(
                DeviceModel.find_by_id(row[0])
            )

        return devices
    
    @property
    def middleware(self):
        if self._middleware: return self._middleware

        self._middleware = MiddlewareModel.find_by_id(self.middleware_id)
        return self._middleware

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into device (model, type, middleware_id) values (?, ?, ?)", (
                self.model, self.type, self.middleware_id
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update device set model=?, type=?, middleware_id=? where id = ?", (
                self.model, self.type, self.middleware_id, self.id
                ))

        conn.close(True)
    

