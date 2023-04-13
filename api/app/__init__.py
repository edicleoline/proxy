import sys
from api.service.servercontrol import ServerControl
from framework.manager.modem import ModemManager
from framework.models.server import ServerModel
from framework.proxy.factory import ProxyService
from framework.service.Cloacker import CloackerService
from framework.service.modem.modemservice import ModemsEventObserver, ModemsService, ModemsAutoRotateService
from framework.service.route.routeservice import RouteService
from framework.service.server.servereventservice import ServerEvent
from framework.settings import Settings

sys.path.append("../")

class Object(object): pass

app = Object

app.settings = Settings()

app.socketio = None

app.cloacker_service = CloackerService(settings = app.settings)

app.server_control = ServerControl(settings = app.settings, socketio = lambda: app.socketio)

app.server_event = ServerEvent(settings = app.settings, socketio = lambda: app.socketio)

server = ServerModel.find_by_id(1)

app.proxy_service = ProxyService(server = server, settings = app.settings)

app.route_service = RouteService(server = server, settings = app.settings)
app.route_service.observe()

app.modems_manager = ModemManager(proxy_service = app.proxy_service, settings = app.settings)

app.modems_service = ModemsService(
    server = server, 
    modems_manager = app.modems_manager,
    settings = app.settings,
    cloacker_service = app.cloacker_service
)
#app.modems_service.observe()

#app.modems_states = []
#def set_modems_states(modems_states): app.modems_states = modems_states
#app.modems_service.subscribe_status(lambda modems_states: set_modems_states(modems_states))
#app.modems_service.subscribe_connectivity(lambda modems_states: set_modems_states(modems_states))

app.modems_event_observer = ModemsEventObserver(
    server_event = app.server_event, 
    settings = app.settings,
    cloacker_service = app.cloacker_service
)
app.modems_service.subscribe_status(lambda modems_states: app.modems_event_observer.observe(modems_states))

app.modems_service.subscribe_status(lambda modems_states: app.route_service.update_modems(modems_states))

app.modems_auto_rotate_service = ModemsAutoRotateService(
    modems_service = app.modems_service, 
    modems_manager = app.modems_manager, 
    server_event = app.server_event,
    settings = app.settings
)
#app.modems_auto_rotate_service.observe()