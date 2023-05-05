from db import connection
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class IpLabelModel():
    id: int
    label: str

    def __init__(self, id = None, label = None, created_at = None):
        self.id = id
        self.label = label
        self.created_at = created_at
    
    @classmethod
    def find_by_id(cls, id):
        conn = connection()
        row = conn.execute("SELECT id, label, created_at FROM ip_label WHERE id=?", (id, )).fetchone()
        conn.close(True)

        if row == None: return None

        return cls(id = row[0], label = row[1], created_at = row[2])
        
    @classmethod
    def find_by_label(cls, label):
        conn = connection()
        row = conn.execute("SELECT id FROM ip_label WHERE label=?", (label, )).fetchone()
        conn.close(True)

        if row == None: return None

        return cls.find_by_id(row[0])
    
    @classmethod
    def all(cls):
        conn = connection()
        rows = conn.execute("SELECT id FROM ip_label ORDER BY created_at DESC").fetchall()
        conn.close(True)

        ip_labels = []
        for row in rows:
            ip_labels.append(cls.find_by_id(row[0]))

        return ip_labels

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("INSERT INTO ip_label (label) values (?)", (
                self.label,
            ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("UPDATE ip_label SET label=? WHERE id = ?", (
                self.label, self.id
            ))

        conn.close(True)

    def delete_from_db(self):
        pass
