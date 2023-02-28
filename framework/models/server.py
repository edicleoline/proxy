from typing import List

from framework.util.database import Database
from framework.models.modem import Modem as MModem

class Server:
    def __init__(self, id = None, installation_id = None, name = None, external_ip = None):
        self.database = Database.get_database()
        self.id = id
        self.installation_id = installation_id
        self.name = name
        self.external_ip = external_ip

    @staticmethod
    def get_by_id(id):
        server = Server(id=id)
        connection = server.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id, installation_id, name, external_ip from server where id = %s', (id))
        row = cursor.fetchone()
        connection.close()
        
        if row == None:
            return None

        return Server(
            id = row[0],
            installation_id = row[1],
            name = row[2],
            external_ip = row[3]
        )    

    @staticmethod
    def get_by_name(name):
        server = Server(name=name)
        connection = server.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id from server where name = %s', (name))
        row = cursor.fetchone()
        connection.close()

        if row == None:
            return None

        return Server.get_by_id(row[0])
    
    def get_usb_ports(self):
        connection = self.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id from usb_port where server_id = %s', (self.id))
        rows = cursor.fetchall()
        connection.close()

        ports = []

        for row in rows:
            ports.append(
                USBPort.get_by_id(row[0])
            )

        return ports

    def get_modems(self):
        connection = self.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select modem_id from modem_server where server_id = %s', (self.id))
        rows = cursor.fetchall()
        connection.close()

        modems = []

        for row in rows:
            modems.append(
                Modem.get_by_server_and_modem(self, MModem.get_by_id(row[0]))
            )

        return modems


class Modem:
    def __init__(self, id = None, server_id = None, modem_id = None, usb_port_id = None, proxy_port = None):
        self.database = Database.get_database()
        self.id = id
        self.server_id = server_id
        self.modem_id = modem_id
        self.usb_port_id = usb_port_id
        self.proxy_port = proxy_port

    def get_modem(self) -> MModem:
        if self.modem_id == None:
            return None

        return MModem.get_by_id(self.modem_id)   

    def get_server(self) -> Server:
        if self.server_id == None:
            return None

        return Server.get_by_id(self.server_id)   

    def get_usb_port(self):
        if self.usb_port_id == None:
            return None

        return USBPort.get_by_id(self.usb_port_id)
        
    @staticmethod
    def get_by_id(id):
        modemServer = Modem(id=id)
        connection = modemServer.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id, server_id, modem_id, usb_port_id, proxy_port from modem_server where id = %s', (id))
        row = cursor.fetchone()
        connection.close()
        
        if row == None:
            return None

        return Modem(
            id = row[0],
            server_id = row[1],
            modem_id = row[2],
            usb_port_id = row[3],
            proxy_port = row[4]
        )

    @staticmethod
    def get_by_server_and_modem(server, modem):
        modemServer = Modem()
        connection = modemServer.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id from modem_server where server_id = %s and modem_id = %s', (server.id, modem.id))
        row = cursor.fetchone()
        connection.close()

        if row == None:
            return None

        return Modem.get_by_id(row[0])
    

USB_STATUS_ON  = 'on'
USB_STATUS_OFF = 'off'

class USBPort:
    def __init__(self, id = None, port: int = 0, status = None):
        self.database = Database.get_database()
        self.id = id
        self.port = port
        self.real_port = port - 1
        self.status = status

    @staticmethod
    def get_by_id(id):
        usb_port = USBPort(id=id)
        connection = usb_port.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id, port, status from usb_port where id = %s', (id))
        row = cursor.fetchone()
        connection.close()
        
        if row == None:
            return None

        return USBPort(
            id = row[0],
            port = int(row[1]),
            status = row[2]
        )
    
    def set_status(self, status):
        connection = Database.get_database().get_db_connection()
        cursor = connection.cursor()
        cursor.execute('UPDATE usb_port SET status =%s WHERE id = %s', (status, self.id))
        connection.commit()
        connection.close()