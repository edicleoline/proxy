import sys
from api.service.servercontrol import ServerControl
from framework.manager.modem import ModemManager
from framework.models.server import ServerModel
from framework.proxy.factory import ProxyService
from framework.service.Cloacker import CloackerService
from framework.service.common.commonservice import CommonService, CommonServiceSubscriberEvent
from framework.service.modem.modemservice import ModemServiceSubscriber, ModemServiceSubscriberEvent, ModemsEventObserver, ModemsService, ModemsAutoRotateService
from framework.service.route.routeservice import RouteService
from framework.service.server.servereventservice import ServerEvent
from framework.service.server.serverservice import ServerService, ServerState
from framework.settings import Settings

sys.path.append("../")

class Object(object): pass

app = Object

app.settings = Settings()

app.socketio = None

app.cloacker_service = CloackerService(settings = app.settings)

app.server_control = ServerControl(settings = app.settings, socketio = lambda: app.socketio)

app.server_event = ServerEvent(settings = app.settings, socketio = lambda: app.socketio)

app.server_service = ServerService(settings = app.settings)
app.server_service.observe()
app.server_service.subscribe(lambda server_state: app.socketio.emit('server_state', ServerState.schema().dump(server_state, many=False), broadcast=True) if app.socketio else None)

server = ServerModel.find_by_id(1)

app.common_service = CommonService(settings = app.settings)
app.common_service.observe()

app.proxy_service = ProxyService(server = server, settings = app.settings)

app.route_service = RouteService(server = server, settings = app.settings)
app.route_service.observe()

app.modems_manager = ModemManager(proxy_service = app.proxy_service, settings = app.settings)

app.modems_service = ModemsService(
    server = server, 
    modems_manager = app.modems_manager,
    settings = app.settings,
    cloacker_service = app.cloacker_service,
    common_service = app.common_service,
    subscribers = [
        ModemServiceSubscriber(ModemServiceSubscriberEvent.ON_MODEMS_RELOAD, lambda modems_states: app.proxy_service.set_modems(modems_states)),
        # ModemServiceSubscriber(ModemServiceSubscriberEvent.ON_MODEMS_STATUS_UPDATED, lambda modems_states: print('updated_subscribe {0}'.format(len(modems_states)))),
        # ModemServiceSubscriber(ModemServiceSubscriberEvent.ON_MODEMS_CONNECTIVITY_UPDATED, lambda modems_states: print('connectivity_subscribe {0}'.format(len(modems_states))))
    ]
)
#app.modems_service.observe()

app.modems_event_observer = ModemsEventObserver(
    server_event = app.server_event, 
    settings = app.settings,
    cloacker_service = app.cloacker_service
)

app.modems_service.subscribe(ModemServiceSubscriberEvent.ON_MODEMS_STATUS_UPDATED, lambda modems_states: app.modems_event_observer.observe(modems_states))
app.modems_service.subscribe(ModemServiceSubscriberEvent.ON_MODEMS_STATUS_UPDATED, lambda modems_states: app.route_service.set_modems(modems_states))

app.modems_auto_rotate_service = ModemsAutoRotateService(
    modems_service = app.modems_service, 
    modems_manager = app.modems_manager, 
    server_event = app.server_event,
    settings = app.settings
)
#app.modems_auto_rotate_service.observe()
