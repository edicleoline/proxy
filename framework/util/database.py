import pymysql

from framework.util.config import Config

class Database:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def get_database():
        return Database(Config)

    def get_db_connection(self):
        try:
            configParser = self.config.get_config_parser()
            return pymysql.connect(
                db = configParser.get('database', 'db'), 
                user = configParser.get('database', 'user'), 
                passwd = configParser.get('database', 'password'), 
                host = configParser.get('database', 'host'), 
                port = configParser.getint('database', 'port'), 
                autocommit = True
            )
        except pymysql.err.OperationalError as e:
            pass