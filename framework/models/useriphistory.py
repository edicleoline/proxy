from db import connection

class UserIPHistory():
    def __init__(self, user, modem_ip_history_id):
        self.user = user
        self.modem_ip_history_id = modem_ip_history_id

    @classmethod
    def is_ip_reserved_for_other(cls, ip, user):
        conn = connection()
        #TODO: SQL count
        rows = conn.execute("select iih.*, uih.* from modem_ip_history iih left join user_ip_history uih ON (uih.modem_ip_history_id = iih.id) where iih.ip = ? and uih.user <> ?", (ip, user)).fetchall()
        conn.close(True)
        return True if len(rows) > 0 else False

    @classmethod
    def get_last_ip(cls, user):
        conn = connection()
        row = conn.execute("select iih.id, iih.ip from user_ip_history uih join modem_ip_history iih ON (iih.id = uih.modem_ip_history_id) where uih.user = ? order by uih.id desc limit 1", (user)).fetchone()
        conn.close(True)
        return row[1] if row else None

    def save_to_db(self):
        conn = connection()
        conn.execute("INSERT INTO user_ip_history (user, modem_ip_history_id) VALUES (?, ?)", (
            self.user, self.modem_ip_history_id
            ))
        self.id = conn.last_insert_rowid
        conn.close(True)