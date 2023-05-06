from db import connection

class ModemIpHistoryModel():
    def __init__(self, modem_id = None, ip = None, network_type = None, network_provider = None, signalbar = None, created_at = None):
        self.modem_id = modem_id
        self.ip = ip
        self.network_type = network_type
        self.network_provider = network_provider
        self.signalbar = signalbar
        self.created_at = created_at         

    def save_to_db(self):
        conn = connection()
        conn.execute("insert into modem_ip_history (modem_id, ip, network_type, network_provider, signalbar) values (?, ?, ?, ?, ?)", (
            self.modem_id, self.ip, self.network_type, self.network_provider, self.signalbar
            ))
        self.id = conn.last_insert_rowid()
        conn.close(True)