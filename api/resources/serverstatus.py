from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from framework.models.server import Server as ServerModel
from models.serverstatus import ServerStatus as ServerStatusModel

class ServerStatus(Resource):
    @jwt_required()
    def get(self):
        server = ServerModel.find_by_id(1)

        if not server:
            return {"message": "Item not found"}, 404

        server_status = ServerStatusModel.get_status(server)
        return server_status.json()

        

    