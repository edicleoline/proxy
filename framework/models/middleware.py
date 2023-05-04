from typing import List
from db import connection
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from framework.models.middlewareparam import MiddlewareParamModel

@dataclass_json
@dataclass
class MiddlewareModel():
    id: int
    name: str
    description: str
    class_name: str  
    params: List[MiddlewareParamModel]
    
    def __init__(self, id = None, name = None, description = None, class_name = None, created_at = None):
        self.id = id
        self.name = name
        self.description = description
        self.class_name = class_name        
        self.created_at = created_at        

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, name, description, class_name, created_at from middleware where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return MiddlewareModel(id = row[0], name = row[1], description = row[2], class_name = row[3], created_at = row[4])
    
    @property
    def params(self):
        return MiddlewareParamModel.find_by_middleware_id(self.id)
    
    @classmethod
    def all(cls):
        conn = connection()
        rows = conn.execute("select id from middleware order by id asc").fetchall()
        conn.close(True)

        devices = []
        for row in rows:
            devices.append(
                MiddlewareModel.find_by_id(row[0])
            )

        return devices

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into middleware (name, description, class_name) values (?, ?, ?)", (
                self.name, self.description, self.class_name
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update middleware set name=?, description=?, class_name=? where id = ?", (
                self.name, self.description, self.class_name, self.id
                ))

        conn.close(True)
    

