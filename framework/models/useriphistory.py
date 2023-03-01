from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import desc

from framework.models.modemiphistory import ModemIPHistory
from db import session, Base

class UserIPHistory(Base):
    __tablename__ = 'user_ip_history'

    id = Column(Integer, primary_key=True)
    user = Column(String(140))
    modem_ip_history_id = Column(Integer, ForeignKey("modem_ip_history.id"), primary_key=False) 
    modem_ip_history = relationship(ModemIPHistory, lazy="joined")   
    
    def json(self):
        return {
            'id': self.id,
            'created_at': self.created_at
        }        

    @classmethod
    def is_ip_reserved_for_other(cls, ip, user):
        t = session.query(UserIPHistory)\
            .join(ModemIPHistory)\
            .filter(UserIPHistory.user != user)\
            .filter(ModemIPHistory.ip == ip)\
            .order_by(desc(UserIPHistory.id)).limit(1).first()
        return True if t != None else False

    @classmethod
    def get_last_ip(cls, user):
        return session.query(UserIPHistory).filter(UserIPHistory.user == user).order_by(desc(UserIPHistory.id)).limit(1).first()    

    def save_to_db(self):
        session.add(self)
        session.commit()