from db import connection

class IpLabelHistoryModel():
    def __init__(self, ip_label_id = None, modem_ip_history_id = None):
        self.ip_label_id = ip_label_id
        self.modem_ip_history_id = modem_ip_history_id

    @classmethod
    def is_ip_reserved_for_other(cls, ip, ip_label_id):
        conn = connection()
        row = conn.execute("""
                SELECT COUNT(*) 
                    FROM modem_ip_history mih 
                    LEFT JOIN ip_label_history puih ON (puih.modem_ip_history_id = mih.id) 
                        WHERE mih.ip = ? AND puih.proxy_user_id <> ?
            """, (ip, ip_label_id)).fetchone()
        conn.close(True)
        return True if int(row[0]) > 0 else False

    def save_to_db(self):
        conn = connection()
        conn.execute("INSERT INTO ip_label_history (proxy_user_id, modem_ip_history_id) VALUES (?, ?)", (
            self.ip_label_id, self.modem_ip_history_id
            ))
        self.id = conn.last_insert_rowid()
        conn.close(True)