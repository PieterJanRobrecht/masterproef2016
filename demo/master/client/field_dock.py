from server.dock import Dock


class FieldDock(Dock):
    def __init__(self, host, port):
        super(FieldDock, self).__init__()
        self.host = host
        self.port = port

    def start_service(self):
        print("FIELD DOCK -- Starting services")
        super(FieldDock, self).start_service()
        print("FIELD DOCK -- Services started")
