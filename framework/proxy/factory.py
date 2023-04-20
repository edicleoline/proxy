from __future__ import annotations
from typing import List
from framework.models.server import ServerModel, ServerModemModel
from framework.settings import Settings

class ProxyService():
    def __init__(self, server: ServerModel, settings: Settings = None, modems: List[ServerModemModel] = []):
        self.server = server
        self.settings = settings
        self.update_modems(modems)

    def update_modems(self, modems: List[ServerModemModel]):
        self.modems = modems

    def resolve(self, modem: ServerModemModel):
        pass

