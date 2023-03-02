from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from db import db

class Installation(db.Model):
    __tablename__ = 'installation'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }

    @classmethod
    def find_by_id(cls, id: int):
        return db.s.query(Installation).filter(Installation.id == id).first()
    

