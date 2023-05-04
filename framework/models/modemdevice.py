from framework.models.device import DeviceModel
from framework.models.modemmiddleware import ModemMiddlewareModel
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class ModemDeviceModel(DeviceModel):
    middleware: ModemMiddlewareModel    

    def __init__(self, id = None, model = None, type = None, middleware_id = None, created_at = None):
        super().__init__(id = id, model = model, type = type, middleware_id = middleware_id, created_at = created_at)
        self.modem_id: int = None

    @classmethod
    def find_by_id(cls, id: int, modem_id: int):
        device_model = super(ModemDeviceModel, cls).find_by_id(id)
        device_model.modem_id = modem_id
        return device_model
    
    @property
    def middleware(self):
        if self._middleware: return self._middleware
        self._middleware = ModemMiddlewareModel.find_by_id(self.middleware_id)
        self._middleware.modem_id = self.modem_id
        return self._middleware