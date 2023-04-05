import sys
from api.service.modems import ModemsService, ModemsAutoRotateService
from api.service.servercontrol import ServerControl
from api.service.serverevent import ServerEvent
from framework.manager.modem import ModemManager
from framework.models.server import ServerModel
from framework.proxy.factory import ProxyService

sys.path.append("../")

class Object(object):
    pass

app = Object

app.socketio = None

app.server_control = ServerControl(socketio = lambda: app.socketio)

app.server_event = ServerEvent(socketio = lambda: app.socketio)

server = ServerModel.find_by_id(1)

app.proxy_service = ProxyService(server = server)

app.modems_manager = ModemManager(proxy_service = app.proxy_service)

app.modems_service = ModemsService(
    server = server, 
    modems_manager = app.modems_manager,
    server_event = app.server_event
)

app.modems_auto_rotate_service = ModemsAutoRotateService(
    modems_service = app.modems_service, 
    modems_manager = app.modems_manager, 
    server_event = app.server_event
)