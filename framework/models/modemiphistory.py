from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from db import session, Base

class ModemIPHistory(Base):
    __tablename__ = 'modem_ip_history'

    id = Column(Integer, primary_key=True)
    modem_id = Column(Integer, ForeignKey("modem.id"), primary_key=False)
    ip = Column(String(15))
    network_type = Column(String(90))
    network_provider = Column(String(90))
    signalbar = Column(String(5))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    
    def json(self):
        return {
            'id': self.id,
            'created_at': self.created_at
        }        

    def save_to_db(self):
        session.add(self)
        session.commit()