from framework.infra.netiface import NetIface
from framework.models.middleware import MiddlewareModel
from framework.settings import Settings
from framework.helper.importlib import class_factory

class MiddlewareFactory():
    def __init__(self, middleware: MiddlewareModel, params: dict, iface: NetIface, settings: Settings):
        self.middleware = middleware
        self.params = params
        self.iface = iface
        self.settings = settings

    def instance(self):
        if self.iface == None or self.iface.ifaddresses == None: return None

        try:
            return class_factory(
                'framework.middleware.module.{0}.{0}'.format(self.middleware.class_name), 
                iface = self.iface, 
                params = self.params, 
                settings = self.settings
            )
        except Exception:
            return None