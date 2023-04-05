from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from framework.models.server import ServerModel, ServerModemModel


class ProxyService():
    def __init__(self, server: ServerModel, modems: List[ServerModemModel] = []):
        self.server = server
        self.update_modems(modems)

    def update_modems(self, modems: List[ServerModemModel]):
        self.modems = modems

    def resolve(self, modem: ServerModemModel):
        pass

