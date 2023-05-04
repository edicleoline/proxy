from framework.models.server import ServerModel, ServerModemModel
from threading import Thread, Event, Lock
from time import sleep
from framework.settings import Settings

class RouteServiceObserverThread(Thread):
    def __init__(self, modems_states = [], stop_event: Event = None):
        self.delay = 3
        self.modems_states = modems_states
        self.stop_event = stop_event
        super(RouteServiceObserverThread, self).__init__()

    def run_forever(self):
        try:
            while not self.stop_event.isSet():
                self._resolve_routes()                
                sleep(self.delay)

        except KeyboardInterrupt:
            # kill()
            pass

    def run(self):
        self.run_forever()

    def _resolve_routes(self):
        if not self.modems_states: return
        
        for modems_state in self.modems_states:
            if modems_state.infra_modem == None: continue
            if modems_state.infra_modem.is_connected() == True:
                modems_state.infra_modem.resolve_route()


class RouteServiceObserver():
    def __init__(self, modems_states):
        self.modems_states = modems_states
        self.lock = Lock()
        self.stop_event = Event()
        self.thread = RouteServiceObserverThread()

    def update_modems(self, modems_states):
        self.modems_states = modems_states
        self.thread.modems_states = self.modems_states

    def start(self):
        with self.lock:
            if not self.thread.is_alive():
                self.thread = RouteServiceObserverThread(modems_states = self.modems_states, stop_event = self.stop_event)
                self.thread.start()

    def stop(self):
        self.stop_event.set()


class RouteService():
    def __init__(self, server: ServerModel, settings: Settings = None, modems_states = []):
        self.server = server
        self.settings = settings
        self.observer = None
        self.modems_states = modems_states
        self.observer = RouteServiceObserver(self.modems_states)

    def set_modems(self, modems_states):
        self.modems_states = modems_states
        self.observer.update_modems(self.modems_states)

    def observe(self):
        self.observer.start()

    def stop_observe(self):
        self.observer.stop()