from db import connection
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class IpLabelFilterModel():
    id: int
    type: str
    value: str
    
    def __init__(self, id = None, ip_label_id = None, modem_id = None, type = None, value = None, created_at = None):
        self.id = id
        self.ip_label_id = ip_label_id
        self.modem_id = modem_id
        self.type = type
        self.value = value
        self.created_at = created_at   
 
    @classmethod
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("""
            SELECT id, ip_label_id, modem_id, filter_type, filter_value, created_at 
                FROM ip_label_filter 
                WHERE id=?""", (id, )).fetchone()
        conn.close(True)

        if row == None: return None

        return cls(
            id = row[0], 
            ip_label_id = row[1], 
            modem_id = row[2], 
            type = row[3], 
            value = row[4], 
            created_at = row[5]
        )
        
    @classmethod
    def find_by_ip_label(cls, ip_label_id: int):
        conn = connection()
        rows = conn.execute("SELECT id FROM ip_label_filter WHERE ip_label_id=?", (ip_label_id, )).fetchall()
        conn.close(True)

        if rows == None: return None
        
        items = []
        for row in rows:
            items.append(IpLabelFilterModel.find_by_id(row[0]))

        return items
    
    @classmethod
    def find_by_ip_label_and_modem(cls, ip_label_id, modem_id):
        conn = connection()
        rows = conn.execute("""
            SELECT id
                FROM ip_label_filter 
                WHERE ip_label_id=? AND modem_id=? 
                GROUP BY filter_value""", (ip_label_id, modem_id)).fetchall()
        conn.close(True)

        if rows == None: return None
        
        items = []        
        for row in rows:            
            items.append(cls.find_by_id(row[0]))

        return items

    def save_to_db(self):
        conn = connection()

        if not self.value or not self.type:
            return False

        if self.id == None:
            conn.execute("INSERT INTO ip_label_filter (ip_label_id, modem_id, filter_type, filter_value) VALUES (?, ?, ?, ?)", (
                self.ip_label_id, self.modem_id, self.type, self.value,
            ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("UPDATE ip_label_filter SET filter_value=? WHERE id = ?", (
                self.value, self.id
            ))

        conn.close(True)

    def delete_from_db(self):
        pass
