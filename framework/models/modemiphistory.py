from signal import signal
from socket import IP_TOS
import pymysql

from framework.util.database import Database

class ModemIpHistory:
    def __init__(self, modem_id, ip, network_type, network_provider, signalbar):
        self.database = Database.get_database()
        self.modem_id = modem_id
        self.ip = ip
        self.network_type = network_type
        self.network_provider = network_provider
        self.signalbar = signalbar

    @staticmethod
    def add(modem_id, ip, network_type, network_provider, signalbar):        
        connection = Database.get_database().get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO modem_ip_history (modem_id, ip, network_type, network_provider, signalbar) VALUES (%s, %s, %s, %s, %s)', (modem_id, ip, network_type, network_provider, signalbar))
        id = cursor.lastrowid
        connection.commit()
        connection.close()
        return id
        
        

    
    