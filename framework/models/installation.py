import pymysql

from framework.util.database import Database

class Installation:
    def __init__(self, id = None, name = None):
        self.database = Database.get_database()
        self.id = id
        self.name = name

    @staticmethod
    def get_by_id(id):
        installation = Installation(id=id)
        connection = installation.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id, name from installation where id = %s', (id))
        row = cursor.fetchone()
        connection.close()
        
        if row == None:
            return None

        return Installation(
            id = row[0],
            name = row[1]
        )

    @staticmethod
    def get_by_name(name):
        installation = Installation(name=name)
        connection = installation.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select id from installation where name = %s', (name))
        row = cursor.fetchone()
        connection.close()

        if row == None:
            return None

        return Installation.get_by_id(row[0])
    