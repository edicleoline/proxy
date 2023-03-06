# from sqla_wrapper import SQLAlchemy

import apsw
import apsw.ext

# db = SQLAlchemy("mysql+pymysql://berners:a1b2z1x2@127.0.0.1/proxy?charset=utf8mb4")
# db = SQLAlchemy("sqlite:////home/berners/Documents/dev/proxy/data.db")

def connection():
    return apsw.Connection("/home/berners/Documents/dev/proxy/data.db")
