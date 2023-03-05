from db import connection

class UserModel():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password    
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_id(cls, id):
        conn = connection()
        row = conn.execute("select id, username, password from user where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return UserModel(id = row[0], username = row[1], password = row[2])

    @classmethod
    def find_by_username(cls, username):
        conn = connection()
        row = conn.execute("select id from user where username=?", (username, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return cls.find_by_id(row[0])

    def save_to_db(self):
        pass

    def delete_from_db(self):
        pass

    def crypt_password(cls, password):
        pass
