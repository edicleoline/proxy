import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from framework.models.middleware import MiddlewareModel
from resources.restresource import RestResource

class Middleware(Resource):
    def get(self, device_id):
        pass
    
class Middlewares(RestResource):
    def get(self):
        middlewares = MiddlewareModel.all()
        return self.dumps(MiddlewareModel, middlewares), 200