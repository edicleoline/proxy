from framework.models.server import Server

class ServerStatus:
    def __init__(self, server: Server):
        self.server = server

    def json(self):
        return {
            'cpu_percent': self.server.cpu_percent(),
            'virtual_memory': self.server.virtual_memory()
        }

    @classmethod
    def get_status(self, server: Server):
        return ServerStatus(server = server)