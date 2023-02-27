from framework.util.database import Database

class UserIpHistory:
    def __init__(self):
        self.database = Database.get_database()

    def is_ip_reserved_for_other(self, ip, user_email):
        connection = self.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select iih.*, uih.* from modem_ip_history iih left join user_ip_history uih ON (uih.modem_ip_history_id = iih.id) where iih.ip = %s and uih.user <> %s', (ip, user_email))
        rows = cursor.fetchall()
        exists = len(rows) > 0
        connection.close()
        return exists

    def get_last_ip(self, user_email):
        connection = self.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select iih.id, iih.ip from user_ip_history uih join modem_ip_history iih ON (iih.id = uih.modem_ip_history_id) where uih.user = %s order by uih.id desc limit 1', (user_email))
        row = cursor.fetchone()
        connection.close()
        return row[1] if row else None
        

    def add(self, user_email, modem_ip_history_id):
        connection = self.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO user_ip_history (user, modem_ip_history_id) VALUES (%s, %s)', (user_email, modem_ip_history_id))
        id = cursor.lastrowid
        connection.commit()
        connection.close()
        return id