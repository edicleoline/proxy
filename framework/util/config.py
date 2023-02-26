import configparser
import os

class Config:
    def __init__(self):
        pass

    @staticmethod
    def get_config_parser():
        configParser = configparser.RawConfigParser()
        configParser.read(os.path.join(os.getcwd(), 'config.ini'))
        return configParser