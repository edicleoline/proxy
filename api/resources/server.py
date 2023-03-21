from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from framework.models.server import ServerModel

class Server(Resource):
    # @jwt_required()
    def get(self):        
        server = ServerModel.find_by_id(1)

        if server:
            return server.json()

        return {"message": "Item not found"}, 404
    

class ServerUSBPorts(Resource):
    # @jwt_required()
    def get(self):        
        server = ServerModel.find_by_id(1)

        if not server:
            return {"message": "Item not found"}, 404
        
        usb_ports = server.usb_ports()

        items = [item.json() for item in usb_ports]
      
        return {"items": items}, 200

    