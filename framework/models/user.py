from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db import db

class UserModel(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(240), nullable=False)
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        return db.s.query(UserModel).filter(UserModel.username == username).first()

    @classmethod
    def find_by_id(cls, _id):
        return db.s.query(UserModel).filter(UserModel.id == id).first()

    def save_to_db(self):
        db.s.add(self)
        db.s.commit()

    def delete_from_db(self):
        db.s.delete(self)
        db.s.commit()
