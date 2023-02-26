import pymysql

from framework.util.database import Database
from framework.models.modemserver import ModemServer
from framework.models.modem import Modem

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
    

    def get_modems(self):
        connection = self.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select modem_id from modem_server where server_id = %s', (self.id))
        rows = cursor.fetchall()
        connection.close()

        modems = []

        for row in rows:
            modems.append(
                ModemServer.get_by_server_and_modem(self, Modem.get_by_id(row[0]))
            )

        return modems
