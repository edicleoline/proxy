import sys
from api.service.modems import ModemsService, ModemsAutoRotateService
from framework.manager.modem import ModemManager
from framework.models.server import ServerModel

sys.path.append("../")

class Object(object):
    pass

app = Object

app.socketio = None

app.modems_manager = ModemManager()

server_model = ServerModel.find_by_id(1)
app.modems_service = ModemsService(server_model = server_model, modems_manager = app.modems_manager)

app.modems_auto_rotate_service = ModemsAutoRotateService(
    modems_service = app.modems_service, 
    modems_manager = app.modems_manager, 
    socketio = lambda: app.socketio
)

app.modems_service.auto_rotate_service = app.modems_auto_rotate_service