from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields
from typing import List
from enum import Enum
import uuid

class TaskWizardStepTypeField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        return TaskWizardStepTypeField[value]
    
task_wizard_step_type_field = {
    "dataclasses_json": {
        "encoder": lambda type: type.name,
        "decoder": lambda name: TaskWizardStepTypeField(name),
        "mm_field": TaskWizardStepTypeField(),
    }
}

class TaskWizardStepType(Enum):
    CHECKING_CONNECTION           = 1
    CHECK_CONNECTION              = 2
    SELECT_INTERFACE              = 3


@dataclass_json
@dataclass
class TaskWizardStep():
    id: str
    type: TaskWizardStepTypeField = field(metadata=task_wizard_step_type_field)
    require_response: bool = False
    response: dict = None

    def __init__(self, type: TaskWizardStepType, require_response: bool = False, response: dict = None):
        self.id = uuid.uuid4()
        self.type = type
        self.require_response = require_response
        self.response = response


@dataclass_json
@dataclass
class TaskWizard():
    steps: List[TaskWizardStep]

    def __init__(self):
        self.steps = []

    def add_step(self, step: TaskWizardStep):
        self.steps.append(step)

    def step_by_id(self, id):
        for step in self.steps:
            if str(step.id) == str(id):
                return step
            
        return None