from db import connection

class ProxyUserModel():
    def __init__(self, id = None, name = None, created_at = None):
        self.id = id
        self.name = name
        self.created_at = created_at
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def find_by_id(cls, id):
        conn = connection()
        row = conn.execute("select id, name, created_at from proxy_user where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return ProxyUserModel(id = row[0], name = row[1], created_at = row[2])
        
    @classmethod
    def find_by_name(cls, name):
        conn = connection()
        row = conn.execute("select id from proxy_user where name=?", (name, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return cls.find_by_id(row[0])

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into proxy_user (name) values (?)", (
                self.name,
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update proxy_user set name=? where id = ?", (
                self.name, self.id
                ))

        conn.close(True)

    def delete_from_db(self):
        pass
