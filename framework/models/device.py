import pymysql

from framework.util.database import Database

class Device:
    def __init__(self, id = None, model = None, type = None):
        self.database = Database.get_database()
        self.id = id
        self.model = model
        self.type = type

    @staticmethod
    def get_by_id(id):
        device = Device(id=id)
        connection = device.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id, model, type from device where id = %s', (id))
        row = cursor.fetchone()
        connection.close()
        
        if row == None:
            return None

        return Device(
            id = row[0],
            model = row[1],
            type = row[2]
        )  
    
    