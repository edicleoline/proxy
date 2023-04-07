from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum
from marshmallow import fields
import json
import uuid

class EventTypeField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        return EventTypeField[value]

server_control_action_field = {
    "dataclasses_json": {
        "encoder": lambda type: type.name,
        "decoder": lambda name: EventType(name),
        "mm_field": EventTypeField(),
    }
}

class EventType(Enum):
    MODEM_LOG    = 'MODEM_LOG'
    UNEXPECTED_MODEM_DISCONNECT = 'UNEXPECTED_MODEM_DISCONNECT'
    MODEM_CONNECT = 'MODEM_CONNECT'


@dataclass_json
@dataclass
class Event():
    id: str
    type: EventType = field(metadata=server_control_action_field)
    data: any

    def __init__(self, type: EventType, data: any):
        self.type = type
        self.data = data
        self.id = self.generate_id()

    def generate_id(self):
        return uuid.uuid4()


class ServerEvent():
    def __init__(self, socketio):
        self.socketio = socketio
    
    def emit(self, event: Event):
        socketio = self.socketio()
        if not socketio:
            return False
        
        socketio.emit('event', json.loads(event.to_json()), broadcast = True)

        return True