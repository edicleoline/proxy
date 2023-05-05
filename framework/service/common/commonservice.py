from typing import List
from framework.models.server import ServerModel, ServerModemModel
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from threading import Thread, Event, Lock
from time import sleep
from framework.settings import Settings
from enum import Enum
import psutil

class CommonServiceSubscriberEvent(Enum):
    ON_NET_CONNECTIONS_UPDATED = 'on_net_connections_updated'


class CommonServiceSubscribe():
    type: CommonServiceSubscriberEvent
    callback = None

    def __init__(self, type: CommonServiceSubscriberEvent, callback):
        self.type = type
        self.callback = callback


class CommonServiceObserver():
    def __init__(self, settings: Settings, subscribers = []):
        self.settings = settings
        self.subscribers = subscribers

    def main(self):
        self.net_connections()

    def net_connections(self):
        connections = psutil.net_connections()
        for subscriber in self.subscribers:
            if subscriber.type == CommonServiceSubscriberEvent.ON_NET_CONNECTIONS_UPDATED: subscriber.callback(connections)


class CommonServiceObserveThread(Thread):
    def __init__(self, service_observer: CommonServiceObserver = None, stop_event: Event = None, delay: int = 1):        
        self.service_observer = service_observer
        self.stop_event = stop_event
        self.delay = delay        
        super(CommonServiceObserveThread, self).__init__()

    def run_forever(self):
        try:
            while not self.stop_event.is_set():
                self.service_observer.main()
                sleep(self.delay)
        except KeyboardInterrupt:
            pass

    def run(self):
        self.run_forever()


class CommonService():
    subscribers: List[CommonServiceSubscribe] = None
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.subscribers = []
        self._service_observe_lock = Lock()
        self._service_observe_stop_event = Event()
        self._service_observe_thread = None        
        self.service_observer = CommonServiceObserver(settings = settings, subscribers = self.subscribers)        

    def observe(self):
        with self._service_observe_lock:
            if not self._service_observe_thread or not self._service_observe_thread.is_alive():
                self._service_observe_thread = CommonServiceObserveThread(
                    service_observer = self.service_observer, 
                    stop_event = self._service_observe_stop_event,
                    delay = self.settings.common_service_interval         
                )
                self._service_observe_thread.start()

    def subscribe(self, type: CommonServiceSubscriberEvent, callback):
        self.subscribers.append(CommonServiceSubscribe(type = type, callback = callback))