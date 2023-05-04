from framework.models.middlewareparam import MiddlewareParamModel
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class ModemMiddlewareParamModel(MiddlewareParamModel):
    value: str

    def __init__(self, id: int = None, middleware_id: int = None, name: str = None, name_translate: str = None, type: str = None, required: bool = True, created_at=None):        
        super().__init__(id, middleware_id, name, name_translate, type, required, created_at)        
        self.modem_id: int = None

    @property
    def value(self):
        return 'value modem_id {0}'.format(self.modem_id)