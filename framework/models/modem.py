from db import connection
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from framework.models.modemdevice import ModemDeviceModel

@dataclass_json
@dataclass
class ModemModel():
    id: int
    imei: str
    addr_id: str
    device: ModemDeviceModel  

    def __init__(self, id = None, imei = None, device_id = None, addr_id = None, created_at = None):
        self.id = id
        self.imei = imei
        self.device_id = device_id
        self._device = None
        self.addr_id = addr_id
        self.created_at = created_at

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, imei, device_id, addr_id, created_at from modem where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return ModemModel(id = row[0], imei = row[1], device_id = row[2], addr_id = row[3], created_at = row[4])

    @property
    def device(self):
        if self._device: return self._device
        self._device = None if self.device_id == None else ModemDeviceModel.find_by_id(id = self.device_id, modem_id = self.id)
        return self._device

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
    

