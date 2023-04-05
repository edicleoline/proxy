from typing import List
from framework.models.server import ServerModel, ServerModemModel
from framework.infra.modem import Modem as IModem
from threading import Thread, Event, Lock
from time import sleep

class RouteServiceObserverThread(Thread):
    def __init__(self, modems: List[ServerModemModel] = [], stop_event: Event = None):
        self.delay = 3
        self.modems = modems
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
        if not self.modems:
            return
        
        for modem in self.modems:
            imodem = IModem(modem)
            if imodem.is_connected() == True:
                imodem.resolve_route()


class RouteServiceObserver():
    def __init__(self, modems: List[ServerModemModel]):
        self.modems = modems
        self.lock = Lock()
        self.stop_event = Event()
        self.thread = RouteServiceObserverThread()

    def update_modems(self, modems: List[ServerModemModel]):
        self.modems = modems
        self.thread.modems = self.modems

    def start(self):
        with self.lock:
            if not self.thread.is_alive():
                self.thread = RouteServiceObserverThread(modems = self.modems, stop_event = self.stop_event)
                self.thread.start()

    def stop(self):
        self.stop_event.set()


class RouteService():
    def __init__(self, server: ServerModel, modems: List[ServerModemModel] = []):
        self.server = server
        self.observer = None
        self.modems = modems
        self.observer = RouteServiceObserver(self.modems)

    def update_modems(self, modems: List[ServerModemModel]):
        self.modems = modems
        self.observer.update_modems(self.modems)

    def resolve(self, modem: ServerModemModel):
        pass

    def observe(self):
        self.observer.start()

    def stop_observe(self):
        self.observer.stop()