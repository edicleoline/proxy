from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from db import db

class Device(db.Model):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    model = Column(String(40))
    type = Column(String(80))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    
    def json(self):
        return {
            'id': self.id,
            'created_at': self.created_at
        }

    @classmethod
    def find_by_id(cls, id: int):
        return db.s.query(Device).filter(Device.id == id).first()
    

