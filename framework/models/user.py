from db import connection
from passlib.hash import pbkdf2_sha256

class UserModel():
    def __init__(self, id = None, username = None, password = None, created_at = None):
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_id(cls, id):
        conn = connection()
        row = conn.execute("select id, username, password, created_at from user where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return UserModel(id = row[0], username = row[1], password = row[2], created_at = row[3])
        
    @classmethod
    def find_by_username(cls, username):
        conn = connection()
        row = conn.execute("select id from user where username=?", (username, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return cls.find_by_id(row[0])

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into user (username, password) values (?, ?)", (
                self.username, self.password
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update user set password=? where id = ?", (
                self.password, self.id
                ))

        conn.close(True)

    def delete_from_db(self):
        pass

    @classmethod
    def crypt_password(cls, password):
        return pbkdf2_sha256.hash(password)
