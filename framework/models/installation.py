from db import connection

class InstallationModel():
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
    def find_by_id(cls, id: int):
        conn = connection()
        row = conn.execute("select id, name, created_at from installation where id=?", (id, )).fetchone()
        conn.close(True)

        if row == None:
            return None

        return InstallationModel(id = row[0], name = row[1], created_at = row[2])

    def save_to_db(self):
        conn = connection()

        if self.id == None:
            conn.execute("insert into installation (name) values (?)", (
                self.name,
                ))
            self.id = conn.last_insert_rowid()
        else:
            conn.execute("update installation set name=? where id = ?", (
                self.name, self.id
                ))

        conn.close(True)
    

