from framework.models.middleware import MiddlewareModel
from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from framework.models.middlewareparam import MiddlewareParamModel

class ModemMiddlewareModel(MiddlewareModel):
    params: List[MiddlewareParamModel]

    @property
    def params(self):
        print('called from ext')
        return None