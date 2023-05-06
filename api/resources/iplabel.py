from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from framework.models.iplabel import IpLabelModel
from framework.models.iplabelfilter import IpLabelFilterModel
from framework.models.server import ServerModel
from models.serverstatus import ServerStatus as ServerStatusModel
from resources.restresource import RestResource

class IpLabel(Resource):
    pass

class IpLabels(RestResource):
    def get(self):
        ip_labels = IpLabelModel.all()
        return self.dumps(IpLabelModel, ip_labels), 200
    

class IpLabelByLabel(RestResource):
    def get(self, ip_label):
        return self.dump(IpLabelModel, IpLabelModel.find_by_label(ip_label)), 200
    

class IpLabelModemFilters(RestResource):
    def get(self, ip_label_id, modem_id):
        filters = IpLabelFilterModel.find_by_ip_label_and_modem(ip_label_id = ip_label_id, modem_id = modem_id)
        return self.dumps(IpLabelFilterModel, filters), 200