from framework.models.middleware import MiddlewareModel
from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from framework.models.middlewareparam import MiddlewareParamModel
from framework.models.modemmiddlewareparam import ModemMiddlewareParamModel

class ModemMiddlewareModel(MiddlewareModel):
    params: List[ModemMiddlewareParamModel]

    @property
    def params(self):
        _params = ModemMiddlewareParamModel.find_by_middleware_id(self.id)
        print('called from ext')
        return _params