from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from framework.models.server import Server as ServerModel
from models.serverstatus import ServerStatus as ServerStatusModel

from framework.infra.modem import Modem as IModem

class ServerModems(Resource):
    @jwt_required()
    def get(self):
        server = ServerModel.find_by_id(1)

        if not server:
            return {"message": "Item not found"}, 404

        modems = server.modems
        
        items = [item.json() for item in modems]

        for x, item in enumerate(items):
            imodem = IModem(modems[x])
            item['is_connected'] = imodem.is_connected()
    
        return {"items": items}, 200


        

    