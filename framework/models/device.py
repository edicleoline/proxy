from db import connection

class DeviceModel():
    def __init__(self, id = None, model = None, type = None, created_at = None):
        self.id = id
        self.model = model
        self.type = type
        self.created_at = created_at    
    
    def json(self):
        return {
            'id': self.id,
            'model': self.model,
            'type': self.type
        }

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, model, type, created_at from device where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return DeviceModel(id = row[0], model = row[1], type = row[2], created_at = row[3])

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into device (model, type) values (?, ?)", (
                self.model, self.type
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update device set model=?, type=? where id = ?", (
                self.model, self.type, self.id
                ))

        conn.close(True)
    

