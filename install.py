import sys
# from flask import Flask, jsonify
# from db import db
# from framework.models.server import Server
# from framework.models.user import UserModel
# from framework.models.device import Device
# from framework.models.installation import Installation
# from framework.models.modem import Modem
# from framework.models.server import USBPort
# from framework.models.server import ServerModem
# from passlib.hash import pbkdf2_sha256
from db import connection

if __name__ == '__main__':    

    conn = connection()

    conn.execute("""
        CREATE TABLE user (
        id INTEGER NOT NULL, 
        username VARCHAR(80) NOT NULL, 
        password VARCHAR(240) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (username)
        )
        """)

    conn.execute("""
        CREATE TABLE installation (
        id INTEGER NOT NULL, 
        name VARCHAR(40), 
        created_at DATETIME NOT NULL, 
        PRIMARY KEY (id)
        )
        """)

    conn.execute("""
        CREATE TABLE server (
        id INTEGER NOT NULL, 
        name VARCHAR(40), 
        installation_id INTEGER, 
        created_at DATETIME NOT NULL, 
        PRIMARY KEY (id)
        )
        """)

    conn.execute("""
        CREATE TABLE usb_port (
        id INTEGER NOT NULL, 
        port INTEGER, 
        status VARCHAR, 
        server_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(server_id) REFERENCES server (id)
        )
        """)

    conn.execute("""
        CREATE TABLE device (
        id INTEGER NOT NULL, 
        model VARCHAR(40), 
        type VARCHAR(80), 
        created_at DATETIME NOT NULL, 
        PRIMARY KEY (id)
        )
        """)

    conn.execute("""
        CREATE TABLE modem (
        id INTEGER NOT NULL, 
        device_id INTEGER, 
        addr_id VARCHAR(15), 
        created_at DATETIME NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(device_id) REFERENCES device (id)
        )
        """)

    conn.execute("""
        CREATE TABLE modem_server (
        id INTEGER NOT NULL, 
        server_id INTEGER, 
        modem_id INTEGER, 
        usb_port_id INTEGER, 
        proxy_port INTEGER, 
        created_at DATETIME, 
        PRIMARY KEY (id), 
        FOREIGN KEY(server_id) REFERENCES server (id), 
        FOREIGN KEY(modem_id) REFERENCES modem (id), 
        FOREIGN KEY(usb_port_id) REFERENCES usb_port (id)
        )
        """)


    conn.close()


    sys.exit(0)
    # db.create_all()

    # user = UserModel()
    # user.username = 'berners'
    # user.password = pbkdf2_sha256.hash('xzxz0909')
    # user.save_to_db()

    # installation = Installation()
    # installation.name = 'barueri-lab'
    # installation.save_to_db()

    # server = Server()
    # server.installation_id = 1
    # server.name = 'raspberry-pi'
    # server.save_to_db()

    # device = Device()
    # device.model = 'MF79S'
    # device.type = '4G_DONGLE'
    # device.save_to_db()

    # usb_ports = [
    #     { 'port': 1, 'status': 'on', 'server_id': 1 },
    #     { 'port': 2, 'status': 'on', 'server_id': 1 },
    #     { 'port': 3, 'status': 'on', 'server_id': 1 },
    #     { 'port': 4, 'status': 'on', 'server_id': 1 },
    #     { 'port': 5, 'status': 'on', 'server_id': 1 },
    #     { 'port': 6, 'status': 'on', 'server_id': 1 },
    #     { 'port': 7, 'status': 'on', 'server_id': 1 },
    #     { 'port': 8, 'status': 'on', 'server_id': 1 },       
    # ]
    # for u in usb_ports:
    #     usb_port = USBPort()
    #     usb_port.port = u['port']
    #     usb_port.status = u['status']
    #     usb_port.server_id = u['server_id']
    #     usb_port.save_to_db()

    # modems = [
    #     { 'device_id': 1, 'addr_id': '10.56.70' },
    #     { 'device_id': 1, 'addr_id': '10.56.71' },
    #     { 'device_id': 1, 'addr_id': '10.56.72' },
    #     { 'device_id': 1, 'addr_id': '10.56.73' },
    #     { 'device_id': 1, 'addr_id': '10.56.74' },
    #     { 'device_id': 1, 'addr_id': '10.56.75' }        
    # ]

    # for m in modems:
    #     modem = Modem()
    #     modem.device_id = m['device_id']
    #     modem.addr_id = m['addr_id']
    #     modem.save_to_db()

    # server_modems = [
    #     { 'server_id': 1, 'modem_id': 1, 'usb_port_id': 7, 'proxy_port': 1025 },
    #     { 'server_id': 1, 'modem_id': 2, 'usb_port_id': 8, 'proxy_port': 1026 },
    #     { 'server_id': 1, 'modem_id': 3, 'usb_port_id': 7, 'proxy_port': 1027 },
    #     { 'server_id': 1, 'modem_id': 4, 'usb_port_id': 5, 'proxy_port': 1028 },
    #     { 'server_id': 1, 'modem_id': 5, 'usb_port_id': 6, 'proxy_port': 1029 },
    #     { 'server_id': 1, 'modem_id': 6, 'usb_port_id': 5, 'proxy_port': 1030 },
    # ]
    # for s in server_modems:
    #     server_modem = ServerModem()
    #     server_modem.server_id = s['server_id']
    #     server_modem.modem_id = s['modem_id']
    #     server_modem.usb_port_id = s['usb_port_id']
    #     server_modem.proxy_port = s['proxy_port']
    #     server_modem.save_to_db()


    # s = Server.find_by_id(1)
    print('done')