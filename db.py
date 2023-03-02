from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
# from flask_sqlalchemy import SQLAlchemy
from sqla_wrapper import SQLAlchemy

engine = create_engine("mysql+pymysql://berners:a1b2z1x2@127.0.0.1/proxy?charset=utf8mb4", echo=False)
session = Session(engine)
Base = declarative_base()

db = SQLAlchemy("mysql+pymysql://berners:a1b2z1x2@127.0.0.1/proxy?charset=utf8mb4")
