from db import connection
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class MiddlewareParamModel():
    id: int
    name: str
    name_translate: str
    type: str
    required: bool    

    def __init__(
        self, id:int = None, 
        middleware_id:int = None, 
        name:str = None, 
        name_translate:str = None, 
        type:str = None, 
        required:bool = True, 
        created_at = None
    ):
        self.id = id
        self.middleware_id = middleware_id
        self.name = name
        self.name_translate = name_translate
        self.type = type
        self.required = required
        self.created_at = created_at        

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, middleware_id, name, name_translate, type, required, created_at from middleware_param where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return cls(
            id = row[0], 
            middleware_id = row[1],
            name = row[2], 
            name_translate = row[3], 
            type = row[4], 
            required = True if row[5] and row[5] == 1 else False, 
            created_at = row[6]
        )
    
    @classmethod
    def find_by_middleware_id(cls, middleware_id):
        conn = connection()
        rows = conn.execute("select id from middleware_param where middleware_id = ? order by id asc", (middleware_id, )).fetchall()
        conn.close(True)

        params = []
        for row in rows:
            params.append(
                cls.find_by_id(row[0])
            )

        return params

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into middleware_param (middleware_id, name, name_translate, type, required) values (?, ?, ?, ?, ?)", (
                self.middleware_id, self.name, self.name_translate, self.type, 1 if self.required and self.required == True else 0
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update middleware_param set name=?, name_translate=?, type=?, required=? where id = ?", (
                self.middleware_id, self.name, self.name_translate, self.type, 1 if self.required and self.required == True else 0, self.id
                ))

        conn.close(True)
    

