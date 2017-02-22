from server.dock import Dock
from server.message import Message


class FieldDock(Dock):
    def __init__(self, host, port):
        super(FieldDock, self).__init__()
        self.host = host
        self.port = port

    def start_service(self):
        print("FIELD DOCK -- Starting services")
        thread = super(FieldDock, self).start_service()
        print("FIELD DOCK -- Services started")
        return thread

    def handle_message(self):
        while True:
            data = self.message_queue.get()
            if Message.check_format(data):
                message = Message.convert_to_message(data)
        # TODO set counter and stuff
