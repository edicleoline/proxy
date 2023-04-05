import sys
from api.service.modems import ModemsService, ModemsAutoRotateService
from api.service.servercontrol import ServerControl
from api.service.serverevent import ServerEvent
from framework.manager.modem import ModemManager
from framework.models.server import ServerModel

sys.path.append("../")

class Object(object):
    pass

app = Object

app.socketio = None

app.server_control = ServerControl(
    socketio = lambda: app.socketio
)

app.server_event = ServerEvent(
    socketio = lambda: app.socketio
)

server_model = ServerModel.find_by_id(1)

app.modems_manager = ModemManager()

app.modems_service = ModemsService(
    server_model = server_model, 
    modems_manager = app.modems_manager,
    server_event = app.server_event
)

app.modems_auto_rotate_service = ModemsAutoRotateService(
    modems_service = app.modems_service, 
    modems_manager = app.modems_manager, 
    server_event = app.server_event
)

app.modems_service.auto_rotate_service = app.modems_auto_rotate_service