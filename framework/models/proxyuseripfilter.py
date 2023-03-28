from db import connection
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class ProxyUserIPFilterModel():
    type: str
    value: str
    
    def __init__(self, id = None, proxy_user_id = None, modem_id = None, type = None, value = None, created_at = None):
        self.id = id
        self.proxy_user_id = proxy_user_id
        self.modem_id = modem_id
        self.type = type
        self.value = value
        self.created_at = created_at   
    
    def json(self):
        return {
            'id': self.id,
            'proxy_user_id': self.proxy_user_id,
            'modem_id': self.modem_id,
            'type': self.type,
            'value': self.value
        }

    @classmethod
    def find_by_id(cls, id):
        conn = connection()
        row = conn.execute("select id, proxy_user_id, modem_id, filter_type, filter_value, created_at from proxy_user_ip_filter where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return ProxyUserIPFilterModel(
            id = row[0], 
            proxy_user_id = row[1], 
            modem_id = row[2], 
            type = row[3], 
            value = row[4], 
            created_at = row[5]
            )
        
    @classmethod
    def find_by_proxy_user(cls, proxy_user_id):
        conn = connection()
        rows = conn.execute("select id from proxy_user_ip_filter where proxy_user_id=?", (proxy_user_id, )).fetchall()
        conn.close(True)

        if rows == None:
            return None
        
        items = []
        for row in rows:
            items.append(
                ProxyUserIPFilterModel.find_by_id(row[0])
            )

        return items
    
    @classmethod
    def find_by_proxy_user_and_modem(cls, proxy_user_id, modem_id):
        conn = connection()
        rows = conn.execute("""select id
            from proxy_user_ip_filter 
                where proxy_user_id=? and modem_id=? GROUP BY filter_value""", (proxy_user_id, modem_id)).fetchall()
        conn.close(True)

        if rows == None:
            return None
        
        items = []
        print(rows)
        for row in rows:            
            items.append(
                ProxyUserIPFilterModel.find_by_id(row[0])
            )

        return items

    def save_to_db(self):
        conn = connection()

        if not self.value or not self.type:
            return False

        if self.id == None:
            conn.execute("insert into proxy_user_ip_filter (proxy_user_id, modem_id, filter_type, filter_value) values (?, ?, ?, ?)", (
                self.proxy_user_id, self.modem_id, self.type, self.value,
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update proxy_user_ip_filter set filter_value=? where id = ?", (
                self.value, self.id
                ))

        conn.close(True)

    def delete_from_db(self):
        pass
