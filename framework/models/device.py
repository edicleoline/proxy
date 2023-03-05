from db import connection

class DeviceModel():
    def __init__(self, id, model, type, created_at):
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
        pass
    

