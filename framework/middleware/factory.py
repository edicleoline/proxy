from framework.infra.netiface import NetIface
from framework.models.middleware import MiddlewareModel
from framework.settings import Settings

from framework.middleware.module.mf79s import MF79S

class MiddlewareFactory():
    def __init__(self, middleware: MiddlewareModel, params: dict, iface: NetIface, settings: Settings):
        self.middleware = middleware
        self.params = params
        self.iface = iface
        self.settings = settings

    def instance(self):
        middleware = MF79S(
            iface = self.iface,
            params = self.params,
            settings = self.settings
        )

        return middleware