from db import connection

class ModemIPHistory():
    def __init__(self, modem_id, ip, network_type, network_provider, signalbar, created_at):
        self.modem_id = modem_id
        self.ip = ip
        self.network_type = network_type
        self.network_provider = network_provider
        self.signalbar = signalbar
        self.created_at = created_at    
    
    def json(self):
        return {
            'id': self.id
        }        

    def save_to_db(self):
        conn = connection()
        conn.execute("insert into modem_ip_history (modem_id, ip, network_type, network_provider, signalbar) values (?, ?, ?, ?, ?)", (
            self.modem_id, self.ip, self.network_type, self.network_provider, self.signalbar
            ))
        self.id = conn.last_insert_rowid
        conn.close(True)