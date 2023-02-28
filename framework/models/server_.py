from datetime import datetime
from enum import Enum
import psutil

from db import session, Base
from framework.models.modem_ import Modem

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    installation_id = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    modems = relationship("ServerModem", back_populates="server", order_by="ServerModem.id")
    usb_ports = relationship("USBPort", order_by="USBPort.id")

    def json(self):
        return {
            'id': self.id,
            'installation_id': self.installation_id,
            'name': self.name,
            'created_at': self.created_at
        }

    @classmethod
    def find_by_id(cls, id: int):
        return session.query(Server).filter(Server.id == id).first()

    @classmethod
    def find_by_name(cls, name):
        return session.query(Server).filter(Server.name == name).first()    

    @staticmethod
    def cpu_percent():
        return psutil.cpu_percent()

    @staticmethod
    def virtual_memory():
        return psutil.virtual_memory()


class ServerModem(Base):
    __tablename__ = 'modem_server'

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey("server.id"), primary_key=False)
    modem_id = Column(Integer, ForeignKey("modem.id"), primary_key=False)
    usb_port_id = Column(Integer, ForeignKey("usb_port.id"), primary_key=False)
    proxy_port = Column(Integer)
    created_at = Column(DateTime)
    modem = relationship(Modem, lazy="joined")
    usb_port = relationship("USBPort", lazy="joined")
    server = relationship("Server", lazy="joined")

    def json(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'created_at': self.created_at
        }

    @classmethod
    def find_by_id(cls, id: int):
        return session.query(ServerModem).filter(ServerModem.id == id).first()

    @classmethod
    def find_by_modem_id(cls, id: int):
        return session.query(ServerModem).filter(ServerModem.modem_id == id).first()


class USBPortStatus(Enum):
    ON  = 'on'
    OFF = 'off'

class USBPort(Base):
    __tablename__ = 'usb_port'

    id = Column(Integer, primary_key=True)
    port = Column(Integer)
    status = Column(String)
    server_id = Column(Integer, ForeignKey("server.id"), primary_key=False)      

    def json(self):
        return {
            'id': self.id,
            'port': self.port,
        }

    @classmethod
    def find_by_id(cls, id: int):
        return session.query(USBPort).filter(USBPort.id == id).first()

    def set_status(self, status:USBPortStatus):
        self.status = status.value
        session.commit()

    def get_status(self):
        return USBPortStatus.ON if self.status == 'on' else USBPortStatus.OFF    

    def get_real_port(self):
        return self.port - 1