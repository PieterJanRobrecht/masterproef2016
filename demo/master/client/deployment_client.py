import gettext
import os.path
from server.message import Message
from SimpleUI import MyApp
from field_dock import FieldDock


def start_field_dock():
    print("FIELD DOCK -- initialisation")
    field_dock = FieldDock('localhost', 54321)
    return field_dock, field_dock.start_service()


def subscribe_to_messages(field_dock):
    d = {"type": ("release", "update")}
    subscribe_message = Message()
    subscribe_message.create_message(field_dock.host, "subscribe", str(d))
    field_dock.send_message(subscribe_message)


def create_file(file_name):
    description_file = open(file_name, 'w+')
    return description_file


def start_description_gui(description_file):
    # TODO make a GUI for the creation of the tower
    print()


def check_description_file(field_dock):
    file_name = "description_file.json"
    if not os.path.isfile(file_name):
        # Creating new description file
        description_file = create_file(file_name)
        # Altering description file with GUI
        start_description_gui(description_file)
        # TODO Sending file to broker or directly to release dock?
        data = description_file.read()
        message = Message()
        message.create_message(field_dock.host, "new", data)
        field_dock.send_message(message)


def connect_to_broker(field_dock):
    print("FIELD DOCK -- Connecting to Broker")
    field_dock.broker_host = 'localhost'
    field_dock.broker_port = 12346
    check_description_file(field_dock)
    subscribe_to_messages(field_dock)
    print("FIELD DOCK -- Subscribed and ready")


def start_gui():
    gettext.install("app")  # replace with the appropriate catalog name
    app = MyApp(0)
    app.MainLoop()


def main():
    field_dock, field_dock_thread = start_field_dock()
    connect_to_broker(field_dock)
    start_gui()

    # Waiting until threads are finished
    field_dock_thread.join()

if __name__ == "__main__":
    main()
