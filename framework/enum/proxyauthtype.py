from enum import Enum
from marshmallow import fields

class ProxyAuthTypeField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name if value else None

    def _deserialize(self, value, attr, data, **kwargs):
        return ProxyAuthTypeField[value] if value else None
    

proxy_auth_type_field = {
    "dataclasses_json": {
        "encoder": lambda type: type.name,
        "decoder": lambda name: ProxyAuthTypeField(name),
        "mm_field": ProxyAuthTypeField(),
    }
}

class ProxyAuthType(Enum):
    NONE  = 'none'
    USER_PASSWORD = 'user_password'