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
    """
        Create a file with specified file name
    :param file_name:
    :return: file
    """
    description_file = open(file_name, 'w+')
    return description_file


def start_description_gui():
    """
        Start the wxPython GUI
        This GUI is used to describe the tower
    :return:
    """
    app = wx.App(False)
    frame = DescriptionCreator(None)
    frame.Show(True)
    app.MainLoop()
    app.Destroy()


def choose_dir():
    """
        Open a directory chooser in wxPython
    :return:
    """
    # app = wx.App(False)
    dialog = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    dialog.Destroy()
    # app.Destroy()
    return path


def receive_file(s, file):
    """
        Receive a file from a socket
    :param s: socket
    :param file:
    :return:
    """
    file_size = int(s.recv(1024))
    while file_size > 0:
        data = s.recv(1024)
        file.write(data)
        file_size -= len(data)


def save_installer_info(installer):
    """
        Save an installer to installer_file.json
    :param installer:
    :return:
    """
    file = open("installer_file.json", "w+")
    file.write(str(installer))


def read_installer_info(field_dock):
    """
        Create installer object from installer_file.json
    :param field_dock:
    :return:
    """
    file = open("installer_file.json", "r+")
    field_dock.current_release = Installer.convert_to_installer(file.read())


class FieldDock(Dock):
    def __init__(self, host, port, release_interface, release_port):
        super(FieldDock, self).__init__()
        # Own parameters for socket
        self.host = host
        self.port = port
        # Parameters for direct communication with release dock
        self.release_interface = release_interface
        self.release_port = release_port
        self.message_thread = None
        self.current_release = None
        self.agents = []
        self.client = None
        # List of actions used to respond to each type of message
        self.actions = {}
        self.initiate_actions()

    def start_service(self):
        """
            Start dock service
            Create a docker client
            Read current installer info if file exists
        :return:
        """
        print("FIELD DOCK -- Starting services")
        thread = super(FieldDock, self).start_service()
        self.init_client()
        # Read installer info from file
        if os.path.exists("installer_file.json"):
            read_installer_info(self)
        print("FIELD DOCK -- Services started")
        return thread

    def init_client(self):
        """
            Create docker client object
        :return:
        """
        env = {"DOCKER_TLS_VERIFY": "1", "DOCKER_HOST": "tcp://192.168.99.100:2376",
               "DOCKER_CERT_PATH": "C:\Users\Pieter-Jan\.docker\machine\machines\default",
               "DOCKER_MACHINE_NAME": "default", "COMPOSE_CONVERT_WINDOWS_PATHS": "true"}
        self.client = docker.from_env(environment=env)

    def handle_message(self):
        """
            Handle all messages in the message queue
            Action performed depend on the actions list
        :return:
        """
        self.message_thread = threading.currentThread()
        while True:
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

    def connect_to_broker(self, sub_dict, broker_interface, broker_port):
        """
            Connect to broker and subscribe
        :param sub_dict: dictionary with types of messages to subscribe
        :return:
        """
        print("FIELD DOCK -- Connecting to Broker")
        super(FieldDock, self).connect_to_broker(sub_dict, broker_interface, broker_port)
        self.check_description_file()
        print("FIELD DOCK -- Subscribed and ready")

    def check_description_file(self):
        """
            Check if description file of the tower exists
            If not start description GUI
        :return:
        """
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
        """
            Deprecated
            Test for ending the message threads, not used
        :return:
        """
        self.message_thread.do_run = False
        self.message_thread.join()

    def unsubscribe_to_messages(self, unsub_dict):
        """
            Unsubscribe to different type of messages
        :param unsub_dict:
        :return:
        """
        unsubscribe_message = Message()
        unsubscribe_message.create_message(self.host, "unsubscribe", unsub_dict)
        self.send_message(unsubscribe_message)

    def perform_release(self, message):
        """
            Convert message data to installer
            Download files directly from release dock
            Download agents from release dock
            Start the install agent
        :param message:
        :return:
        """
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
        host = self.release_interface  # Get local machine name
        port = self.release_port
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
        """
            Send change message to release dock
        :param installer:
        :return:
        """
        print("FIELD DOCK -- Sending change message")
        save_installer_info(installer)
        data = {"idInstaller": installer.id_installer, "name": installer.name, "version": installer.version}
        message = Message()
        message.create_message(self.host, "change", str(data))
        self.send_message(message)

    def kill_containers(self):
        """
            Stop the field, old and quarantine container
        :return:
        """
        try:
            self.client.containers.get("fieldcontainer").stop()
            self.client.containers.get("old_container").stop()
            self.client.containers.get("quarantined").stop()
        except docker.errors.NotFound:
            print("FIELD DOCK -- Could not find one of the containers")
        except requests.exceptions.Timeout:
            print("FIELD DOCK -- Timeout error while trying to stop the containers")
