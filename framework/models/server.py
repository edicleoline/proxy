from enum import Enum
from framework.models.installation import InstallationModel
# import psutil

from framework.models.modem import ModemModel
from db import connection

class ServerModel():
    def __init__(self, id = None, name = None, installation_id = None, created_at = None):
        self.id = id
        self.name = name
        self.installation_id = installation_id
        self.created_at = created_at

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'installation_id': self.installation_id
        }

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, name, installation_id, created_at from server where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return ServerModel(id = row[0], name = row[1], installation_id = row[2], created_at = row[3])

    def usb_ports(self):
        conn = connection()
        rows = conn.execute("select id from usb_port where server_id=?", (self.id, )).fetchall()
        conn.close(True)

        usb_ports = []
        for row in rows:
            usb_ports.append(
                USBPortModel.find_by_id(row[0])
            )

        return usb_ports

    def modems(self):
        conn = connection()
        rows = conn.execute("select id from modem_server where server_id=?", (self.id, )).fetchall()
        conn.close(True)

        modems = []
        for row in rows:
            modems.append(
                ServerModemModel.find_by_id(row[0])
            )

        return modems

    def installation(self):
        return None if self.installation_id == None else InstallationModel.find_by_id(self.installation_id)

    @staticmethod
    def cpu_percent():
        # return psutil.cpu_percent()
        return 1

    @staticmethod
    def virtual_memory():
        # return psutil.virtual_memory()
        return 1

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into server (installation_id, name) values (?, ?)", (
                self.installation_id, self.name
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update server set name=? where id = ?", (
                self.name, self.id
                ))

        conn.close(True)


class USBPortStatus(Enum):
    ON  = 'on'
    OFF = 'off'


class USBPortModel():
    def __init__(self, id = None, port = None, status = None, server_id = None):
        self.id = id
        self.port = port
        self.status = status
        self.server_id = server_id

    def json(self):
        return {
            'id': self.id,
            'port': self.port,
            'status': self.get_status(),
            'server_id': self.server_id
        }

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, port, status, server_id from usb_port where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return USBPortModel(id = row[0], port = row[1], status = row[2], server_id = row[3])

    def set_status(self, status:USBPortStatus):
        self.status = status.value

    def get_status(self):
        return USBPortStatus.ON if self.status == 'on' else USBPortStatus.OFF    

    def get_real_port(self):
        return self.port - 1

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into usb_port (port, status, server_id) values (?, ?, ?)", (
                self.port, self.status, self.server_id
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update usb_port set status=? where id = ?", (
                self.status, self.id
                ))

        conn.close(True)

class ServerModemModel():
    def __init__(self, id = None, server_id = None, modem_id = None, usb_port_id = None, proxy_port = None, created_at = None):
        self.id = id
        self.server_id = server_id
        self.modem_id = modem_id
        self.usb_port_id = usb_port_id
        self.proxy_port = proxy_port
        self.created_at = created_at

    def json(self):
        usb_port = self.usb_port()
        modem = self.modem()
        device = modem.device()
        return {
            'id': self.id,
            # 'server_id': self.server_id,
            'usb': {
                'id': usb_port.id,
                'port': usb_port.port,
                'status': usb_port.status
            },
            'proxy': {
                'port': self.proxy_port
            },
            'modem': {
                'id': modem.id,
                'addr_id': modem.addr_id,
                'device': {
                    'id': device.id,
                    'model': device.model,
                    'type': device.type
                },
            }
            # 'created_at': self.created_at
        }

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, server_id, modem_id, usb_port_id, proxy_port, created_at from modem_server where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return ServerModemModel(id=row[0], server_id=row[1], modem_id=row[2], usb_port_id=row[3], proxy_port=row[4], created_at=row[3])

    @classmethod
    def find_by_modem_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id from modem_server where modem_id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return cls.find_by_id(row[0])

    def usb_port(self):
        return None if self.usb_port_id == None else USBPortModel.find_by_id(self.usb_port_id)

    def server(self):
        return None if self.server_id == None else ServerModel.find_by_id(self.server_id)

    def modem(self):
        return None if self.modem_id == None else ModemModel.find_by_id(self.modem_id)

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into modem_server (server_id, modem_id, usb_port_id, proxy_port) values (?, ?, ?, ?)", (
                self.server_id, self.modem_id, self.usb_port_id, self.proxy_port
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update modem_server set usb_port_id=? where id = ?", (
                self.usb_port_id, self.id
                ))

        conn.close(True)


