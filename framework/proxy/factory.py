from __future__ import annotations
from typing import List
from framework.models.server import ServerModel, ServerModemModel
from framework.settings import Settings

class ProxyService():
    def __init__(self, server: ServerModel, settings: Settings = None):
        self.server = server
        self.settings = settings
        self.modems_states = None

    def set_modems(self, modems_states):
        self.modems_states = modems_states
        self.resolve()

    # def resolve(self, modem: ServerModemModel):
    #     pass

    def resolve(self):
        print('resolve proxy_service')
        for m in self.modems_states:
            print(m.modem.proxy)
        print('resolve proxy_service############################')

