from framework.models.middleware import MiddlewareModel

class ModemMiddlewareModel(MiddlewareModel):
    @property
    def params(self):
        return super(ModemMiddlewareModel, self).find_by_middleware_id(self.id)