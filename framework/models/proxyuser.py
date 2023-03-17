from db import connection

class ProxyUserModel():
    def __init__(self, id = None, username = None, created_at = None):
        self.id = id
        self.username = username
        self.created_at = created_at
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_id(cls, id):
        conn = connection()
        row = conn.execute("select id, username, created_at from proxy_user where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return ProxyUserModel(id = row[0], username = row[1], created_at = row[2])
        
    @classmethod
    def find_by_username(cls, username):
        conn = connection()
        row = conn.execute("select id from proxy_user where username=?", (username, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return cls.find_by_id(row[0])
    
    @classmethod
    def all(cls):
        conn = connection()
        rows = conn.execute("select id from proxy_user order by created_at desc").fetchall()
        conn.close(True)

        proxy_users = []
        for row in rows:
            proxy_users.append(
                ProxyUserModel.find_by_id(row[0])
            )

        return proxy_users

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into proxy_user (username) values (?)", (
                self.username,
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update proxy_user set username=? where id = ?", (
                self.username, self.id
                ))

        conn.close(True)

    def delete_from_db(self):
        pass
