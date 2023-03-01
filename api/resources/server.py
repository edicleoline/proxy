from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from framework.models.server import Server as ServerModel

class Server(Resource):
    @jwt_required()
    def get(self):
        server = ServerModel.find_by_id(1)

        if server:
            return server.json()

        return {"message": "Item not found"}, 404

    