import sys
from framework.enum.proxyauthtype import ProxyAuthType
from framework.models.middleware import MiddlewareModel
from framework.models.middlewareparam import MiddlewareParamModel
from framework.models.server import ServerModel
from framework.models.user import UserModel
from framework.models.device import DeviceModel
from framework.models.installation import InstallationModel
from framework.models.modem import ModemModel
from framework.models.server import USBPortModel
from framework.models.server import ServerModemModel
from db import connection
from apsw import SQLError, ConstraintError

if __name__ == '__main__':    

    conn = connection()

    try:
        conn.execute("""
            CREATE TABLE user (
            id INTEGER NOT NULL, 
            username VARCHAR(80) NOT NULL, 
            password VARCHAR(240) NOT NULL, 
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id), 
            UNIQUE (username)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE installation (
            id INTEGER NOT NULL, 
            name VARCHAR(80), 
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id),
            UNIQUE (name)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE server (
            id INTEGER NOT NULL, 
            name VARCHAR(40), 
            installation_id INTEGER NOT NULL, 
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE usb_port (
            id INTEGER NOT NULL, 
            port INTEGER, 
            status VARCHAR, 
            server_id INTEGER, 
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id), 
            FOREIGN KEY(server_id) REFERENCES server (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE middleware (
            id INTEGER NOT NULL, 
            name VARCHAR(80), 
            class_name VARCHAR(80), 
            description VARCHAR(80), 
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE middleware_param (
            id INTEGER NOT NULL, 
            middleware_id INTEGER,
            name VARCHAR(40),
            name_translate VARCHAR(80), 
            type VARCHAR(20),
            required INTEGER NOT NULL DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id),
            FOREIGN KEY(middleware_id) REFERENCES middleware (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE device (
            id INTEGER NOT NULL, 
            model VARCHAR(40), 
            type VARCHAR(80), 
            middleware_id INTEGER,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id),
            UNIQUE (model, type),
            FOREIGN KEY(middleware_id) REFERENCES middleware (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE modem (
            id INTEGER NOT NULL, 
            imei VARCHAR(40), 
            device_id INTEGER, 
            addr_id VARCHAR(15),             
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id), 
            UNIQUE (addr_id)
            FOREIGN KEY(device_id) REFERENCES device (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE modem_middleware_param (
            id INTEGER NOT NULL, 
            modem_id INTEGER, 
            middleware_param_id INTEGER,   
            value VARCHAR(240),
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id), 
            UNIQUE (modem_id, middleware_param_id)
            FOREIGN KEY(modem_id) REFERENCES modem (id),
            FOREIGN KEY(middleware_param_id) REFERENCES middleware_param (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE modem_server (
            id INTEGER NOT NULL, 
            server_id INTEGER, 
            modem_id INTEGER, 
            usb_port_id INTEGER,
            proxy_auth_type VARCHAR(15),
            proxy_ipv4_http_port INTEGER,
            proxy_ipv4_socks_port INTEGER,
            proxy_ipv6_http_port INTEGER,
            proxy_ipv6_socks_port INTEGER,
            prevent_same_ip_users INTEGER NOT NULL DEFAULT 1,
            auto_rotate INTEGER NOT NULL DEFAULT 0,
            auto_rotate_time INTEGER,
            auto_rotate_hard_reset INTEGER NOT NULL DEFAULT 1,
            auto_rotate_filter VARCHAR(240),            
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id), 
            FOREIGN KEY(server_id) REFERENCES server (id), 
            FOREIGN KEY(modem_id) REFERENCES modem (id), 
            FOREIGN KEY(usb_port_id) REFERENCES usb_port (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE modem_ip_history (
            id INTEGER NOT NULL, 
            modem_id INTEGER NOT NULL, 
            ip VARCHAR(15) NOT NULL, 
            network_type VARCHAR(90),
            network_provider VARCHAR(90),
            signalbar VARCHAR(5),
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id), 
            FOREIGN KEY(modem_id) REFERENCES modem (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE ip_label (
            id INTEGER NOT NULL, 
            label VARCHAR(90) NOT NULL, 
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (id),
            UNIQUE (label)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE ip_label_filter (
            id INTEGER NOT NULL, 
            ip_label_id INTEGER NOT NULL, 
            modem_id INTEGER NOT NULL, 
            filter_type VARCHAR(15) NOT NULL,    
            filter_value VARCHAR(90) NOT NULL,    
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,                    
            PRIMARY KEY (id), 
            FOREIGN KEY(ip_label_id) REFERENCES ip_label (id),
            FOREIGN KEY(modem_id) REFERENCES modem (id)
            )
            """)
    except SQLError:
        pass

    try:
        conn.execute("""
            CREATE TABLE ip_label_history (
            id INTEGER NOT NULL, 
            ip_label_id INTEGER NOT NULL, 
            modem_ip_history_id INTEGER NOT NULL,                         
            PRIMARY KEY (id), 
            FOREIGN KEY(modem_ip_history_id) REFERENCES modem_ip_history (id),
            FOREIGN KEY(ip_label_id) REFERENCES ip_label (id)
            )
            """)
    except SQLError:
        pass    

    try:
        conn.execute("""
            CREATE TABLE modem_log (
            id INTEGER NOT NULL, 
            modem_id INTEGER NOT NULL, 
            owner INTEGER NOT NULL,
            type INTEGER NOT NULL,
            message VARCHAR(240) NOT NULL, 
            code INTEGER, 
            params_json VARCHAR(240), 
            auto INTEGER NOT NULL DEFAULT 0,
            description VARCHAR(240), 
            logged_at DATETIME NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,                    
            PRIMARY KEY (id), 
            FOREIGN KEY(modem_id) REFERENCES modem (id)
            )
            """)
    except SQLError:
        pass
    
    conn.close(True)
    
    try:        
        user_model = UserModel(username = 'berners', password = UserModel.crypt_password('xzxz0909'))
        user_model.save_to_db()
        # print(user.id)
    except ConstraintError:
        pass

    try:
        installation_model = InstallationModel(name = 'Barueri-LAB')
        installation_model.save_to_db()
    except ConstraintError:
        pass

    try:
        server_model = ServerModel(name = 'Raspberry-PI', installation_id = 1)
        server_model.save_to_db()
    except ConstraintError:
        pass

    try:
        usb_ports = [
            { 'port': 1, 'status': 'on', 'server_id': 1 },
            { 'port': 2, 'status': 'on', 'server_id': 1 },
            { 'port': 3, 'status': 'on', 'server_id': 1 },
            { 'port': 4, 'status': 'on', 'server_id': 1 },
            { 'port': 5, 'status': 'on', 'server_id': 1 },
            { 'port': 6, 'status': 'on', 'server_id': 1 },
            { 'port': 7, 'status': 'on', 'server_id': 1 },
            { 'port': 8, 'status': 'on', 'server_id': 1 },       
        ]
        for u in usb_ports:
            usb_port_model = USBPortModel(port = u['port'], status = u['status'], server_id = u['server_id'])
            usb_port_model.save_to_db()
    except ConstraintError:
        pass

    try:
        middlewares = [
            { 'name': 'ZTE MF79S', 'class_name': 'mf79s', 'description': 'app.middleware.model.mf79s.description' },
            { 'name': 'ZTE MF79S 2', 'class_name': 'mf79s', 'description': 'app.middleware.model.mf79s.description' },            
            { 'name': 'Huawei E3372h', 'class_name': 'e3372h', 'description': 'app.middleware.model.e3372h.description' },
            { 'name': 'Android', 'class_name': 'android', 'description': 'app.middleware.model.android.description' }
        ]
        for d in middlewares:
            middleware_model = MiddlewareModel(name = d['name'], description = d['description'], class_name = d['class_name'])
            middleware_model.save_to_db()
    except ConstraintError:
        pass

    try:
        middleware_params = [            
            { 'middleware_id': 1, 'name': 'password', 'name_translate': 'password', 'type': 'str', 'required': True },
            { 'middleware_id': 2, 'name': 'username', 'name_translate': 'username', 'type': 'str', 'required': True },
            { 'middleware_id': 2, 'name': 'password', 'name_translate': 'password', 'type': 'str', 'required': True },
        ]
        for d in middleware_params:
            middleware_param_model = MiddlewareParamModel(middleware_id = d['middleware_id'], name = d['name'], name_translate = d['name_translate'], type = d['type'], required = d['required'])
            middleware_param_model.save_to_db()
    except ConstraintError:
        pass

    try:
        devices = [
            { 'model': 'MF79S', 'type': '4G_DONGLE', 'middleware_id': 1 },
            { 'model': 'MF79S 2', 'type': '4G_DONGLE', 'middleware_id': 2 }            
        ]
        for d in devices:
            device_model = DeviceModel(model = d['model'], type = d['type'], middleware_id = d['middleware_id'])
            device_model.save_to_db()
    except ConstraintError:
        pass

    try:
        modems = [
            { 'imei': '499981121636715', 'device_id': 2, 'addr_id': '10.56.70' },
            { 'imei': '535189163974632', 'device_id': 1, 'addr_id': '10.56.71' },
            { 'imei': '998381769962604', 'device_id': 1, 'addr_id': '10.56.72' },
            { 'imei': '331972696716018', 'device_id': 1, 'addr_id': '10.56.73' },
            { 'imei': '528107331157293', 'device_id': 1, 'addr_id': '10.56.74' },
            { 'imei': '527534278422839', 'device_id': 1, 'addr_id': '10.56.75' },
            { 'imei': '527534278422840', 'device_id': 1, 'addr_id': '10.56.76' },
            { 'imei': '527534278422841', 'device_id': 1, 'addr_id': '10.56.77' }
        ]

        for m in modems:
            modem = ModemModel(imei = m['imei'], device_id = m['device_id'], addr_id = m['addr_id'])
            modem.save_to_db()      
            if m['device_id'] == 1:
                params = modem.device.middleware.params
                params[0].value = 'vivo'
                params[0].save_to_db()
            elif m['device_id'] == 2:
                params = modem.device.middleware.params
                params[0].value = 'claro'
                params[0].save_to_db()
                params[1].value = 'claro_pass'
                params[1].save_to_db()

    except ConstraintError:
        pass

    try:
        server_modems = [
            { 'server_id': 1, 'modem_id': 1, 'usb_port_id': 7, 'proxy_ipv4_http_port': 1025, 'proxy_ipv4_socks_port': 2025, 'proxy_ipv6_http_port': 3025, 'proxy_ipv6_socks_port': 4025, 'proxy_auth_type': ProxyAuthType.NONE },
            { 'server_id': 1, 'modem_id': 2, 'usb_port_id': 8, 'proxy_ipv4_http_port': 1026, 'proxy_ipv4_socks_port': 2026, 'proxy_ipv6_http_port': 3026, 'proxy_ipv6_socks_port': 4026, 'proxy_auth_type': ProxyAuthType.USER_PASSWORD },
            { 'server_id': 1, 'modem_id': 3, 'usb_port_id': 7, 'proxy_ipv4_http_port': 1027, 'proxy_ipv4_socks_port': 2027, 'proxy_ipv6_http_port': 3027, 'proxy_ipv6_socks_port': 4027, 'proxy_auth_type': ProxyAuthType.NONE },
            { 'server_id': 1, 'modem_id': 4, 'usb_port_id': 5, 'proxy_ipv4_http_port': 1028, 'proxy_ipv4_socks_port': 2028, 'proxy_ipv6_http_port': 3028, 'proxy_ipv6_socks_port': 4028, 'proxy_auth_type': ProxyAuthType.NONE },
            { 'server_id': 1, 'modem_id': 5, 'usb_port_id': 6, 'proxy_ipv4_http_port': 1029, 'proxy_ipv4_socks_port': 2029, 'proxy_ipv6_http_port': 3029, 'proxy_ipv6_socks_port': 4029, 'proxy_auth_type': ProxyAuthType.NONE },
            { 'server_id': 1, 'modem_id': 6, 'usb_port_id': 5, 'proxy_ipv4_http_port': 1030, 'proxy_ipv4_socks_port': 2030, 'proxy_ipv6_http_port': 3030, 'proxy_ipv6_socks_port': 4030, 'proxy_auth_type': ProxyAuthType.NONE },
            { 'server_id': 1, 'modem_id': 7, 'usb_port_id': 7, 'proxy_ipv4_http_port': 1031, 'proxy_ipv4_socks_port': 2031, 'proxy_ipv6_http_port': 3031, 'proxy_ipv6_socks_port': 4031, 'proxy_auth_type': ProxyAuthType.NONE },
            { 'server_id': 1, 'modem_id': 8, 'usb_port_id': 8, 'proxy_ipv4_http_port': 1032, 'proxy_ipv4_socks_port': 2032, 'proxy_ipv6_http_port': 3032, 'proxy_ipv6_socks_port': 4032, 'proxy_auth_type': ProxyAuthType.NONE },
        ]
        for s in server_modems:
            server_modem_model = ServerModemModel(
                server_id = s['server_id'], 
                modem_id = s['modem_id'], 
                usb_port_id = s['usb_port_id'], 
                proxy_ipv4_http_port = s['proxy_ipv4_http_port'],
                proxy_ipv4_socks_port = s['proxy_ipv4_socks_port'],
                proxy_ipv6_http_port = s['proxy_ipv6_http_port'],
                proxy_ipv6_socks_port = s['proxy_ipv6_socks_port'],
                prevent_same_ip_users=True,
                auto_rotate=False,
                auto_rotate_time=None,
                proxy_auth_type=s['proxy_auth_type']
                )            
            server_modem_model.save_to_db()

    except ConstraintError:
        pass


   