import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from typing import List, TypeVar, Type

T = TypeVar("T")

class RestResource(Resource):

    def dumps(self, type: Type[T], items: List):
        items_json = type.schema().dumps(items, many=True)
        return {
            "items": json.loads(items_json)
        }