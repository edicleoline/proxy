import sys, os
from api.socketservice.modems import ModemsService
from framework.manager.modem import ModemManager
from framework.models.server import ServerModel

sys.path.append("../")

class Object(object):
    pass

app = Object

app.modems_manager = ModemManager()

server_model = ServerModel.find_by_id(1)
app.modems_service = ModemsService(server_model = server_model, modems_manager = app.modems_manager)