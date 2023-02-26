import pymysql

from framework.util.database import Database
from framework.models.modem import Modem

class ModemServer:
    def __init__(self, id = None, server_id = None, modem_id = None, usb_port = None, proxy_port = None):
        self.database = Database.get_database()
        self.id = id
        self.server_id = server_id
        self.modem_id = modem_id
        self.usb_port = usb_port
        self.proxy_port = proxy_port

    def get_modem(self):
        if self.modem_id == None:
            return None

        return Modem.get_by_id(self.modem_id)     
        
    @staticmethod
    def get_by_id(id):
        modemServer = ModemServer(id=id)
        connection = modemServer.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id, server_id, modem_id, usb_port, proxy_port from modem_server where id = %s', (id))
        row = cursor.fetchone()
        connection.close()
        
        if row == None:
            return None

        return ModemServer(
            id = row[0],
            server_id = row[1],
            modem_id = row[2],
            usb_port = row[3],
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
    