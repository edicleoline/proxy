import pymysql

from framework.util.database import Database
from framework.models.modem import Modem
from framework.models.usbport import USBPort
from framework.models.server import Server

class ModemServer:
    def __init__(self, id = None, server_id = None, modem_id = None, usb_port_id = None, proxy_port = None):
        self.database = Database.get_database()
        self.id = id
        self.server_id = server_id
        self.modem_id = modem_id
        self.usb_port_id = usb_port_id
        self.proxy_port = proxy_port

    def get_modem(self) -> Modem:
        if self.modem_id == None:
            return None

        return Modem.get_by_id(self.modem_id)   

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
        modemServer = ModemServer(id=id)
        connection = modemServer.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id, server_id, modem_id, usb_port_id, proxy_port from modem_server where id = %s', (id))
        row = cursor.fetchone()
        connection.close()
        
        if row == None:
            return None

        return ModemServer(
            id = row[0],
            server_id = row[1],
            modem_id = row[2],
            usb_port_id = row[3],
            proxy_port = row[4]
        )

    @staticmethod
    def get_by_server_and_modem(server, modem):
        modemServer = ModemServer()
        connection = modemServer.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id from modem_server where server_id = %s and modem_id = %s', (server.id, modem.id))
        row = cursor.fetchone()
        connection.close()

        if row == None:
            return None

        return ModemServer.get_by_id(row[0])
    