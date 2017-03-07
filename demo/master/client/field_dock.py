import threading
import urllib

import wx
import os.path

from client.description_file_impl import DescriptionCreator
from server.dock import Dock
from server.installer import Installer
from server.message import Message


def create_file(file_name):
    description_file = open(file_name, 'w+')
    return description_file


def start_description_gui():
    app = wx.App(False)
    frame = DescriptionCreator(None)
    frame.Show(True)
    app.MainLoop()
    app.Destroy()


def choose_dir():
    app = wx.PySimpleApp()
    dialog = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    dialog.Destroy()
    return path


class FieldDock(Dock):
    def __init__(self, host, port):
        super(FieldDock, self).__init__()
        self.host = host
        self.port = port
        self.message_thread = None
        self.actions = {}
        self.initiate_actions()

    def start_service(self):
        print("FIELD DOCK -- Starting services")
        thread = super(FieldDock, self).start_service()
        print("FIELD DOCK -- Services started")
        return thread

    def handle_message(self):
        self.message_thread = threading.currentThread()
        while getattr(self.message_thread, "do_run", True):
            data = self.message_queue.get()
            if Message.check_format(data):
                # TODO set counter and stuff
                # Unpack notification
                message = Message.convert_to_message(data)
                relayed_message = message.data
                # Convert to message
                relayed_message = Message.convert_to_message(relayed_message)
                self.actions[relayed_message.message_type](relayed_message)

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
            start_description_gui()

            data = description_file.read()
            message = Message()
            message.create_message(self.host, "new", data)
            self.send_message(message)

    def kill_message_thread(self):
        self.message_thread.do_run = False
        self.message_thread.join()

    def unsubscribe_to_messages(self, unsub_dict):
        unsubscribe_message = Message()
        unsubscribe_message.create_message(self.host, "unsubscribe", unsub_dict)
        self.send_message(unsubscribe_message)

    def perform_release(self, message):
        print("FIELD DOCK -- Performing new release action")
        message_data = message.data
        installer = Installer.convert_to_tower(message_data)
        # Download files
        testfile = urllib.URLopener()
        src_url = message.sender + installer.disk_location + "release.zip"
        dest_url = choose_dir()
        testfile.retrieve(src_url, dest_url)
        # Download agents
        # Start correct agent

    def perform_update(self, message):
        print("update")

    def initiate_actions(self):
        self.actions["release"] = self.perform_release
        self.actions["update"] = self.perform_update
