from enum import Enum
from typing import List


class ModemManagerSubscriberEvent(Enum):
    ON_ROTATE_SUCCESS = 'on_rotate_success'
    
class ModemManagerSubscriber:
    event: ModemManagerSubscriberEvent
    callback: None

    def __init__(self, event: ModemManagerSubscriberEvent, callback):
        self.event = event
        self.callback = callback

    @classmethod
    def notify(cls, subscribers: List, event: ModemManagerSubscriberEvent, data: any):
        for subscriber in subscribers:
            if subscriber.event == event: subscriber.callback(data)


