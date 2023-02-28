import pymysql

from framework.util.database import Database

class USBPort:
    def __init__(self, id = None, port = None, status = None):
        self.database = Database.get_database()
        self.id = id
        self.port = port
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
    
    