from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from framework.models.proxyuser import ProxyUserModel
from framework.models.proxyuseripfilter import ProxyUserIPFilterModel

from framework.models.server import ServerModel
from models.serverstatus import ServerStatus as ServerStatusModel

class ProxyUser(Resource):
    pass

class ProxyUsers(Resource):
    def get(self):
        proxy_users = ProxyUserModel.all()
        items = [item.json() for item in proxy_users]

        return {"items": items}, 200


class ProxyUserByUsername(Resource):
    def get(self, username):
        proxy_user = ProxyUserModel.find_by_username(username = username)

        if proxy_user == None:
            return {"items": []}, 200

        return proxy_user.json()


class ProxyUserModemFilters(Resource):
    def get(self, proxy_user_id, modem_id):
        filters = ProxyUserIPFilterModel.find_by_proxy_user_and_modem(proxy_user_id = proxy_user_id, modem_id = modem_id)

        if filters == None:
            return {"items": []}, 200

        items = [item.json() for item in filters]

        return {"items": items}, 200