from enum import Enum
import json
from framework.models.installation import InstallationModel
from framework.models.proxyuseripfilter import ProxyUserIPFilterModel
import psutil
from framework.models.modem import ModemModel
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime
from marshmallow import fields
from db import connection
from framework.models.schedule import ModemsAutoRotateAgendaItem

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
            'installation_id': self.installation_id,
            'internal_ip': self.internal_ip(),
            'external_ip': self.external_ip()
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
        return psutil.cpu_percent()

    @staticmethod
    def virtual_memory():
        return psutil.virtual_memory()

    @classmethod
    def external_ip(cls):
        return '127.0.0.1'

    @classmethod
    def internal_ip(cls):
        return 'localhost'

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into server (installation_id, name) values (?, ?)", (
                self.installation_id, self.name
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update server set installation_id=?, name=? where id = ?", (
                self.installation_id, self.name, self.id
                ))

        conn.close(True)


class USBPortStatusField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        return USBPortStatusField[value]
    
usb_port_status_type_field = {
    "dataclasses_json": {
        "encoder": lambda type: type.name,
        "decoder": lambda name: USBPortStatusField(name),
        "mm_field": USBPortStatusField(),
    }
}

class USBPortStatus(Enum):
    ON  = 'on'
    OFF = 'off'

@dataclass_json
@dataclass
class USBPortModel():
    id: int
    port: int  
    status: USBPortStatus = field(metadata=usb_port_status_type_field)

    def __init__(self, id = None, port = None, status = None, server_id = None):
        self.id = id
        self.port = port
        self.status = status
        self.server_id = server_id

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, port, status, server_id from usb_port where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return USBPortModel(id = row[0], port = row[1], status = USBPortStatus(row[2]), server_id = row[3])   

    def get_real_port(self):
        return self.port - 1
    
    def set_status(self, status: USBPortStatus):
        self.status = status

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into usb_port (port, status, server_id) values (?, ?, ?)", (
                self.port, self.status.value, self.server_id
            ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update usb_port set status=? where id = ?", (
                self.status.value, self.id
            ))

        conn.close(True)

@dataclass_json
@dataclass
class ServerModemModel():
    id: int
    usb: USBPortModel
    modem: ModemModel
    prevent_same_ip_users: bool = None
    auto_rotate: bool = None
    auto_rotate_time: int = None
    auto_rotate_hard_reset: bool = None
    auto_rotate_filter: ProxyUserIPFilterModel = None
    schedule: ModemsAutoRotateAgendaItem = None
    proxy: dict

    def __init__(
            self, id = None, 
            server_id = None, 
            modem_id = None, 
            usb_port_id = None, 
            proxy_ipv4_http_port = None, 
            proxy_ipv4_socks_port = None, 
            proxy_ipv6_http_port = None, 
            proxy_ipv6_socks_port = None, 
            prevent_same_ip_users = True,
            auto_rotate = False,
            auto_rotate_time = None,
            auto_rotate_hard_reset = True,
            auto_rotate_filter = None,
            schedule: ModemsAutoRotateAgendaItem = None,
            created_at = None
        ):
        self.id = id
        self.server_id = server_id
        self.modem_id = modem_id
        self._modem = None
        self.usb_port_id = usb_port_id
        self._usb = None
        self.proxy_ipv4_http_port = proxy_ipv4_http_port
        self.proxy_ipv4_socks_port = proxy_ipv4_socks_port
        self.proxy_ipv6_http_port = proxy_ipv6_http_port
        self.proxy_ipv6_socks_port = proxy_ipv6_socks_port
        self.prevent_same_ip_users = prevent_same_ip_users
        self.auto_rotate = auto_rotate
        self.auto_rotate_time = auto_rotate_time
        self.auto_rotate_hard_reset = auto_rotate_hard_reset
        self.auto_rotate_filter = auto_rotate_filter
        self.schedule = schedule
        self.created_at = created_at

    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("""
            SELECT 
                id, 
                server_id, 
                modem_id, 
                usb_port_id, 
                proxy_ipv4_http_port, 
                proxy_ipv4_socks_port, 
                proxy_ipv6_http_port, 
                proxy_ipv6_socks_port, 
                prevent_same_ip_users,
                auto_rotate,
                auto_rotate_time,
                auto_rotate_hard_reset,
                auto_rotate_filter,
                created_at 
                    FROM modem_server 
                    WHERE id=?""", 
            (
                id, 
            )
        ).fetchone()
        conn.close(True)

        if row == None:
            return None

        return ServerModemModel(
            id=row[0], 
            server_id=row[1], 
            modem_id=row[2], 
            usb_port_id=row[3], 
            proxy_ipv4_http_port=row[4], 
            proxy_ipv4_socks_port=row[5], 
            proxy_ipv6_http_port=row[6], 
            proxy_ipv6_socks_port=row[7], 
            prevent_same_ip_users=True if row[8] and int(row[8]) == 1 else False,
            auto_rotate=True if row[9] and int(row[9]) == 1 else False,
            auto_rotate_time=row[10],
            auto_rotate_hard_reset=True if row[11] and int(row[11]) == 1 else False,
            auto_rotate_filter=ProxyUserIPFilterModel.schema().loads(row[12], many=True) if row[12] != None else None
            # created_at=row[11]
        )

    @classmethod
    def find_by_modem_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id from modem_server where modem_id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return cls.find_by_id(row[0])
    
    @property
    def proxy(self):
        return {
            'ipv4': {
                'http': {
                    'port': self.proxy_ipv4_http_port
                },
                'socks': {
                    'port': self.proxy_ipv4_socks_port
                }                    
            },
            'ipv6': {
                'http': {
                    'port': self.proxy_ipv6_http_port
                },
                'socks': {
                    'port': self.proxy_ipv6_socks_port
                }                    
            }      
        }

    @property
    def usb(self):
        if self._usb: return self._usb
        self._usb = None if self.usb_port_id == None else USBPortModel.find_by_id(self.usb_port_id)    
        return self._usb

    def server(self):
        return None if self.server_id == None else ServerModel.find_by_id(self.server_id)

    @property
    def modem(self):
        if self._modem: return self._modem
        self._modem = None if self.modem_id == None else ModemModel.find_by_id(self.modem_id)
        return self._modem

    def save_to_db(self):
        conn = connection()

        if self.auto_rotate_filter:
            self.auto_rotate_filter[:] = [x for x in self.auto_rotate_filter if x.value]

        if self.id == None:
            conn.execute("""
                INSERT INTO
                    modem_server (
                        server_id, 
                        modem_id, 
                        usb_port_id, 
                        proxy_ipv4_http_port, 
                        proxy_ipv4_socks_port, 
                        proxy_ipv6_http_port, 
                        proxy_ipv6_socks_port,
                        prevent_same_ip_users,
                        auto_rotate,
                        auto_rotate_time,
                        auto_rotate_hard_reset,
                        auto_rotate_filter
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (
                    self.server_id, 
                    self.modem_id, 
                    self.usb_port_id, 
                    self.proxy_ipv4_http_port,
                    self.proxy_ipv4_socks_port,
                    self.proxy_ipv6_http_port,
                    self.proxy_ipv6_socks_port,
                    1 if self.prevent_same_ip_users == True else 0,
                    1 if self.auto_rotate == True else 0,
                    int(self.auto_rotate_time) if self.auto_rotate_time else None,
                    1 if self.auto_rotate_hard_reset == True else 0,
                    ProxyUserIPFilterModel.schema().dumps(self.auto_rotate_filter, many=True) if self.auto_rotate_filter else None
                )
            )
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("""
                UPDATE 
                    modem_server SET
                        usb_port_id=?, 
                        proxy_ipv4_http_port=?, 
                        proxy_ipv4_socks_port=?, 
                        prevent_same_ip_users=?,
                        auto_rotate=?,
                        auto_rotate_time=?,
                        auto_rotate_hard_reset=?,
                        auto_rotate_filter=?
                            WHERE id = ?""", 
                (
                    self.usb_port_id, 
                    self.proxy_ipv4_http_port, 
                    self.proxy_ipv4_socks_port, 
                    1 if self.prevent_same_ip_users == True else 0,
                    1 if self.auto_rotate == True else 0,
                    int(self.auto_rotate_time) if self.auto_rotate_time else None,
                    1 if self.auto_rotate_hard_reset == True else 0,
                    ProxyUserIPFilterModel.schema().dumps(self.auto_rotate_filter, many=True) if self.auto_rotate_filter else None,
                    self.id
                )
            )

        conn.close(True)
