from dock import Dock


class Broker(Dock):
    def __init__(self, host, port):
        super(Broker, self).__init__()
        self.host = host
        self.port = port

    def start_service(self):
        print("BROKER -- Starting services")
        thread = super(Broker, self).start_service()
        print("BROKER -- Services started")
        return thread
