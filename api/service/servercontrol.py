from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from enum import Enum
from marshmallow import fields
import json
import uuid

class ServerControlActionField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        return ServerControlActionField[value]

server_control_action_field = {
    "dataclasses_json": {
        "encoder": lambda type: type.name,
        "decoder": lambda name: ServerControlAction(name),
        "mm_field": ServerControlActionField(),
    }
}

class ServerControlAction(Enum):
    RELOAD_MODEM    = 'RELOAD_MODEM'
    # INFO       = 1    

@dataclass_json
@dataclass
class ServerControlEvent():
    id: str
    action: ServerControlAction = field(metadata=server_control_action_field)
    data: any

    def __init__(self, action: ServerControlAction, data: any):
        self.action = action
        self.data = data
        self.id = self.generate_id()

    def generate_id(self):
        return uuid.uuid4()


class ServerControl():
    def __init__(self, socketio):
        self.socketio = socketio
    
    def emit(self, event: ServerControlEvent):
        socketio = self.socketio()
        if not socketio:
            return False
        
        socketio.emit('server_control', json.loads(event.to_json()), broadcast = True)

        return True