from framework.infra.netiface import NetIface
from framework.models.middleware import MiddlewareModel
from framework.settings import Settings

from framework.helper.importlib import class_factory
from framework.middleware.module.mf79s import mf79s

class MiddlewareFactory():
    def __init__(self, middleware: MiddlewareModel, params: dict, iface: NetIface, settings: Settings):
        self.middleware = middleware
        self.params = params
        self.iface = iface
        self.settings = settings

    def instance(self):
        if self.iface == None or self.iface.ifaddresses == None: return None

        class_factory('framework.middleware.module.mf79s', self.iface, self.params, self.settings)

        middleware = mf79s(
            iface = self.iface,
            params = self.params,
            settings = self.settings
        )

        return middleware