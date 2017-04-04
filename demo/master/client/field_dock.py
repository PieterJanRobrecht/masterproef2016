import threading
import socket
import dill
import wx
import os.path
import docker
import requests.exceptions
import docker.errors

from description_file_impl import DescriptionCreator
from server.dock import Dock
from server.install_agent import InstallAgent
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
    # app = wx.App(False)
    dialog = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    dialog.Destroy()
    # app.Destroy()
    return path


def receive_file(s, file):
    file_size = int(s.recv(1024))
    while file_size > 0:
        data = s.recv(1024)
        file.write(data)
        file_size -= len(data)


def save_installer_info(installer):
    file = open("installer_file.json", "w+")
    file.write(str(installer))


def read_installer_info(field_dock):
    file = open("installer_file.json", "r+")
    field_dock.current_release = Installer.convert_to_installer(file.read())


class FieldDock(Dock):
    def __init__(self, host, port):
        super(FieldDock, self).__init__()
        self.host = host
        self.port = port
        self.message_thread = None
        self.current_release = None
        self.agents = []
        self.client = None
        self.actions = {}
        self.initiate_actions()

    def start_service(self):
        print("FIELD DOCK -- Starting services")
        thread = super(FieldDock, self).start_service()
        self.init_client()
        # Read installer info from file
        if os.path.exists("installer_file.json"):
            read_installer_info(self)
        print("FIELD DOCK -- Services started")
        return thread

    def init_client(self):
        # Make new docker container
        env = {"DOCKER_TLS_VERIFY": "1", "DOCKER_HOST": "tcp://192.168.99.100:2376",
               "DOCKER_CERT_PATH": "C:\Users\Pieter-Jan\.docker\machine\machines\default",
               "DOCKER_MACHINE_NAME": "default", "COMPOSE_CONVERT_WINDOWS_PATHS": "true"}
        self.client = docker.from_env(environment=env)

    def handle_message(self):
        self.message_thread = threading.currentThread()
        while getattr(self.message_thread, "do_run", True):
            data = self.message_queue.get()
            print("FIELD DOCK -- Handling message")
            if Message.check_format(data):
                # TODO: retrieving messages that were send during downtime
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
        print("FIELD DOCK -- Performing action: RELEASE")
        message_data = message.data
        installer = Installer.convert_to_installer(message_data)
        self.current_release = installer

        # Download files
        file_dir = choose_dir()
        release_zip = os.path.join(file_dir, "release.zip")
        file = open(release_zip, 'wb+')
        print("FIELD DOCK -- Release zip made")
        s = socket.socket()  # Create a socket object
        host = "localhost"  # Get local machine name
        port = 12346
        s.connect((host, port))
        receive_file(s, file)
        print("FIELD DOCK -- Received release, ready to install")
        file.close()

        # Download agents
        print("FIELD DOCK -- Downloading agents")
        s.send("Ready")
        length = s.recv(1024)
        s.send("Received length")
        file_size = int(str(length))
        data = s.recv(file_size)
        list_agents = dill.loads(data)
        self.agents = list_agents
        s.close()
        print("FIELD DOCK -- Downloaded all the agents")

        # Start correct agent
        for agent in self.agents:
            agent.field_dock = self
            if type(agent) is InstallAgent:
                agent.release_zip_location = file_dir
                agent.action(self.client)

    def perform_update(self, message):
        # TODO
        print("update")

    def initiate_actions(self):
        self.actions["release"] = self.perform_release
        self.actions["update"] = self.perform_update

    def update_info_installer(self, installer):
        print("FIELD DOCK -- Sending change message")
        save_installer_info(installer)
        data = {"idInstaller": installer.id_installer, "name": installer.name, "version": installer.version}
        message = Message()
        message.create_message(self.host, "change", str(data))
        self.send_message(message)

    def kill_containers(self):
        try:
            self.client.containers.get("fieldcontainer").stop()
            self.client.containers.get("old_container").stop()
            self.client.containers.get("quarantined").stop()
        except docker.errors.NotFound:
            print("FIELD DOCK -- Could not find one of the containers")
        except requests.exceptions.Timeout:
            print("FIELD DOCK -- Timeout error while trying to stop the containers")
