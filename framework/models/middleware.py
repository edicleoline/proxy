from db import connection
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class MiddlewareModel():
    id: int
    name: str
    class_name: str  
    def __init__(self, id = None, name = None, class_name = None, created_at = None):
        self.id = id
        self.name = name
        self.class_name = class_name        
        self.created_at = created_at        

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, name, class_name, created_at from middleware where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return MiddlewareModel(id = row[0], name = row[1], class_name = row[2], created_at = row[3])
    
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
            conn.execute("insert into middleware (name, class_name) values (?, ?)", (
                self.name, self.class_name
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update middleware set name=?, class_name=? where id = ?", (
                self.name, self.class_name, self.id
                ))

        conn.close(True)
    

