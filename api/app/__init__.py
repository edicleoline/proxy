import sys
from api.service.modems import ModemsEventObserver, ModemsService, ModemsAutoRotateService
from api.service.servercontrol import ServerControl
from api.service.serverevent import ServerEvent
from framework.manager.modem import ModemManager
from framework.models.server import ServerModel
from framework.proxy.factory import ProxyService
from framework.service.route.routeservice import RouteService

sys.path.append("../")

class Object(object):
    pass

app = Object

app.socketio = None

app.server_control = ServerControl(socketio = lambda: app.socketio)

app.server_event = ServerEvent(socketio = lambda: app.socketio)

server = ServerModel.find_by_id(1)

app.proxy_service = ProxyService(server = server)

app.route_service = RouteService(server = server)
app.route_service.observe()

app.modems_manager = ModemManager(proxy_service = app.proxy_service)

app.modems_service = ModemsService(
    server = server, 
    modems_manager = app.modems_manager,
    route_service = app.route_service
)

app.modems_event_observer = ModemsEventObserver(server_event = app.server_event)
app.modems_service.subscribe_modems_states(lambda modems_states: app.modems_event_observer.observe(modems_states))

# app.modems_service.subscribe_modems_states(lambda modems_states: app.route_service.update_modems(modems_states))

app.modems_auto_rotate_service = ModemsAutoRotateService(
    modems_service = app.modems_service, 
    modems_manager = app.modems_manager, 
    server_event = app.server_event
)