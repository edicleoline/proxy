from framework.models.device import DeviceModel
from db import connection

class ModemModel():
    def __init__(self, id = None, imei = None, device_id = None, addr_id = None, created_at = None):
        self.id = id
        self.imei = imei
        self.device_id = device_id
        self.addr_id = addr_id
        self.created_at = created_at
    
    def json(self):
        return {
            'id': self.id,
            'imei': self.imei,
            'device_id': self.device_id,
            'addr_id': self.addr_id
        }

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, imei, device_id, addr_id, created_at from modem where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return ModemModel(id = row[0], imei = row[1], device_id = row[2], addr_id = row[3], created_at = row[4])

    def device(self):
        return None if self.device_id == None else DeviceModel.find_by_id(self.device_id)

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into modem (imei, device_id, addr_id) values (?, ?, ?)", (
                self.imei, self.device_id, self.addr_id
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update modem set imei=?, device_id=?, addr_id=? where id = ?", (
                self.imei, self.device_id, self.addr_id, self.id
                ))

        conn.close(True)
    

