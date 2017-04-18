import sys
import docker
import docker.errors
import description_file_gui
from threading import Thread
import requests.exceptions


def locate_framework(packages):
    """
        Locate framework package in list of packages
    :param packages:
    :return:
    """
    for package in packages:
        if package.is_framework == 1:
            help_package = package
    return help_package


def start_framework_container(client, framework_package):
    """
        Start fielcontainer
        Send exec command to use start_script in the container
    :param client:
    :param framework_package:
    :return:
    """
    package_folder = framework_package.name + framework_package.version
    try:
        container = client.containers.get("fieldcontainer")
        container.start()
    except docker.errors.NotFound:
        print("MAINGUI -- Container not found, maybe you should install a framework?")

    script_location = "/usr/test/" + package_folder + "/meta/start_script.py"
    command = "python " + script_location
    exe_start = container.exec_run(command, stream=True)
    for val in exe_start:
        print (val)

    try:
        container.stop()
    except docker.errors.APIError:
        print("MAINGUI -- Encountered problem with closing the container")
    except requests.exceptions.Timeout:
        print("MAINGUI -- Timeout occurred")


class MainGui(description_file_gui.MyFrame3):
    def __init__(self, parent, field_dock, field_dock_thread):
        description_file_gui.MyFrame3.__init__(self, parent)
        self.field_dock = field_dock
        self.field_dock_thread = field_dock_thread

    def close_action(self, event):
        """
            Send unsubscribe message
            Kill the necessary containers
        :param event:
        :return:
        """
        print("FIELD DOCK -- Shutting down")
        # Send unsubcribe message
        unsub_dict = {"type": ["release", "update"]}
        self.field_dock.unsubscribe_to_messages(unsub_dict)
        self.field_dock.kill_containers()
        # Kill GUI
        self.Destroy()
        sys.exit(0)

    def start_framework(self, event):
        """
            Locate framework package
            Start thread that handles the container actions
        :param event:
        :return:
        """
        print("MAINGUI -- Starting application")
        client = self.field_dock.client

        framework_package = locate_framework(self.field_dock.current_release.packages)
        framework_thread = Thread(target=start_framework_container, args=(client, framework_package))
        framework_thread.daemon = True
        framework_thread.start()
        # framework_thread.join()

    def manage_packages(self, event):
        # TODO
        print("Manage installed packages")

    def handle_message(self, event):
        # TODO
        print("Handle messages")

    def install_release(self, event):
        # TODO
        print("Install release")
