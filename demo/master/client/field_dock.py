import gettext
import os.path

from description_file_creator import DescriptionGui
from server.dock import Dock
from server.message import Message


def create_file(file_name):
    description_file = open(file_name, 'w+')
    return description_file


def start_description_gui(description_file):
    gettext.install("description") # replace with the appropriate catalog name
    description = DescriptionGui(0)
    description.MainLoop()


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

    def connect_to_broker(self, sub_dict):
        print("FIELD DOCK -- Connecting to Broker")
        super(FieldDock, self).connect_to_broker(sub_dict)
        self.check_description_file()
        print("FIELD DOCK -- Subscribed and ready")

    def check_description_file(self):
        file_name = "description_file.json"
        if not os.path.isfile(file_name):
            # Creating new description file
            description_file = create_file(file_name)
            # Altering description file with GUI
            start_description_gui(description_file)
            # TODO Sending file to broker or directly to release dock?
            data = description_file.read()
            message = Message()
            message.create_message(self.host, "new", data)
            self.send_message(message)
