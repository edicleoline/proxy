from framework.models.server import ServerModel, ServerModemModel
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from threading import Thread, Event, Lock
from time import sleep
from framework.settings import Settings
import psutil

@dataclass_json
@dataclass
class ServerState():
    external_ip: str
    cpu_percent: float
    virtual_memory: dict

    def __init__(self, external_ip: str, cpu_percent: float, virtual_memory: any):
        self.external_ip = external_ip
        self.cpu_percent = cpu_percent
        self.virtual_memory = virtual_memory


class ServerObserver():
    def __init__(self, settings: Settings, subscribers = []):
        self.settings = settings
        self.subscribers = subscribers

    def status(self):
        virtual_memory = psutil.virtual_memory()

        server_state = ServerState(
            external_ip = '200.165.20.31',
            cpu_percent = psutil.cpu_percent(),
            virtual_memory = {
                'total': virtual_memory.total,
                'available': virtual_memory.available,
                'percent': virtual_memory.percent,
                'used': virtual_memory.used,
                'free': virtual_memory.free,
                'active': virtual_memory.active,
                'inactive': virtual_memory.inactive,
                'cached': virtual_memory.cached,
                'shared': virtual_memory.shared,
                'slab': virtual_memory.slab
            }
        )

        for subscriber in self.subscribers:
            subscriber(server_state)


class ServerObserveThread(Thread):
    def __init__(self, server_observer: ServerObserver = None, stop_event: Event = None, delay: int = 1):        
        self.server_observer = server_observer
        self.stop_event = stop_event
        self.delay = delay        
        super(ServerObserveThread, self).__init__()

    def run_forever(self):
        try:
            while not self.stop_event.is_set():
                self.server_observer.status()
                sleep(self.delay)
        except KeyboardInterrupt:
            pass

    def run(self):
        self.run_forever()


class ServerService():
    def __init__(self, settings: Settings):
        self.settings = settings
        self.subscribers = []
        self._server_observe_lock = Lock()
        self._server_observe_stop_event = Event()
        self._server_observe_thread = None        
        self.server_observer = ServerObserver(settings = settings, subscribers = self.subscribers)        

    def observe(self):
        with self._server_observe_lock:
            if not self._server_observe_thread or not self._server_observe_thread.is_alive():
                self._server_observe_thread = ServerObserveThread(
                    server_observer = self.server_observer, 
                    stop_event = self._server_observe_stop_event,
                    delay = self.settings.server_service_state_update_interval         
                )
                self._server_observe_thread.start()

    def subscribe(self, callback):
        self.subscribers.append(callback)