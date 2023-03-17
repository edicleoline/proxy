from db import connection

class ProxyUserIPHistoryModel():
    def __init__(self, proxy_user_id = None, modem_ip_history_id = None):
        self.proxy_user_id = proxy_user_id
        self.modem_ip_history_id = modem_ip_history_id

    @classmethod
    def is_ip_reserved_for_other(cls, ip, proxy_user_id):
        conn = connection()
        row = conn.execute("""
                select count(*) 
                    from modem_ip_history mih 
                    left join proxy_user_ip_history puih ON (puih.modem_ip_history_id = mih.id) 
                        where mih.ip = ? and puih.proxy_user_id <> ?
            """, (ip, proxy_user_id)).fetchone()
        conn.close(True)
        return True if int(row[0]) > 0 else False

    @classmethod
    def get_last_ip(cls, proxy_user_id):
        conn = connection()
        row = conn.execute("select iih.id, iih.ip from user_ip_history uih join modem_ip_history iih ON (iih.id = uih.modem_ip_history_id) where uih.user = ? order by uih.id desc limit 1", (user,)).fetchone()
        conn.close(True)
        return row[1] if row else None

    def save_to_db(self):
        conn = connection()
        conn.execute("INSERT INTO proxy_user_ip_history (proxy_user_id, modem_ip_history_id) VALUES (?, ?)", (
            self.proxy_user_id, self.modem_ip_history_id
            ))
        self.id = conn.last_insert_rowid()
        conn.close(True)