from framework.models.middleware import MiddlewareModel
from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from framework.models.middlewareparam import MiddlewareParamModel
from framework.models.modemmiddlewareparam import ModemMiddlewareParamModel

@dataclass_json
@dataclass
class ModemMiddlewareModel(MiddlewareModel):
    params: List[ModemMiddlewareParamModel]

    def __init__(self, id = None, name = None, description = None, class_name = None, created_at = None):
        super().__init__(id = id, name = name, description = description, class_name = class_name, created_at = created_at)
        self.modem_id: int = None

    @property
    def params(self):
        _params = ModemMiddlewareParamModel.find_by_middleware_id(self.id)
        if _params:
            for param in _params: param.modem_id = self.modem_id
        
        return _params