from framework.models.device import DeviceModel
from framework.models.modemmiddlewaremodel import ModemMiddlewareModel

class ModemDeviceModel(DeviceModel):
    middleware: ModemMiddlewareModel
    modem_id: int = None

    @classmethod
    def find_by_id(cls, id: int, modem_id: int):
        device_model = super(ModemDeviceModel, cls).find_by_id(id)
        device_model.modem_id = modem_id
        return device_model