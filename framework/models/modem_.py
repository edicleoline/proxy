from datetime import datetime

from db import session, Base
from framework.models.device_ import Device

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Modem(Base):
    __tablename__ = 'modem'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("device.id"), primary_key=False)
    addr_id = Column(String(15))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    device = relationship(Device, lazy="joined")
    
    def json(self):
        return {
            'id': self.id,
            'created_at': self.created_at
        }

    @classmethod
    def find_by_id(cls, id: int):
        return session.query(Modem).filter(Modem.id == id).first()
    

