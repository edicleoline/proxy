import pymysql

from framework.util.database import Database

class Modem:
    def __init__(self, id = None, device_id = None, addr_id = None):
        self.database = Database.get_database()
        self.id = id
        self.device_id = device_id
        self.addr_id = addr_id

    @staticmethod
    def get_by_id(id):
        modem = Modem(id=id)
        connection = modem.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id, device_id, addr_id from modem where id = %s', (id))
        row = cursor.fetchone()
        connection.close()
        
        if row == None:
            return None

        return Modem(
            id = row[0],
            device_id = row[1],
            addr_id = row[2]
        )

    
    