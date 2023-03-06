from framework.models.device import DeviceModel
from db import connection

class ModemModel():
    def __init__(self, id = None, device_id = None, addr_id = None, created_at = None):
        self.id = id
        self.device_id = device_id
        self.addr_id = addr_id
        self.created_at = created_at
    
    def json(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'addr_id': self.addr_id
        }

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, device_id, addr_id , created_at from modem where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return ModemModel(id = row[0], device_id = row[1], addr_id = row[2], created_at = row[3])

    def device(self):
        return None if self.device_id == None else DeviceModel.find_by_id(self.device_id)

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into modem (device_id, addr_id) values (?, ?)", (
                self.device_id, self.addr_id
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update modem set addr_id=? where id = ?", (
                self.addr_id, self.id
                ))

        conn.close(True)
    

