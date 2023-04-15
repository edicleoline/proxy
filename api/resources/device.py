import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from framework.models.device import DeviceModel
from framework.models.server import ServerModel
from models.serverstatus import ServerStatus as ServerStatusModel
from resources.restresource import RestResource

class Device(Resource):
    def get(self, device_id):
        pass
    
class Devices(RestResource):
    def get(self):
        devices = DeviceModel.all()
        return self.dumps(DeviceModel, devices), 200