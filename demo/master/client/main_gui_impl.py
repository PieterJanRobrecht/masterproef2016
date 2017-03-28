import sys
import docker
import docker.errors
import description_file_gui


def locate_framework(packages):
    for package in packages:
        if package.is_framework == 1:
            help_package = package
    return help_package


class MainGui(description_file_gui.MyFrame3):
    def __init__(self, parent, field_dock, field_dock_thread):
        description_file_gui.MyFrame3.__init__(self, parent)
        self.field_dock = field_dock
        self.field_dock_thread = field_dock_thread

    def close_action(self, event):
        print("FIELD DOCK -- Shutting down")
        # Send unsubcribe message
        unsub_dict = {"type": ["release", "update"]}
        self.field_dock.unsubscribe_to_messages(unsub_dict)
        # Kill GUI
        self.Destroy()
        sys.exit(0)

    def start_framework(self, event):
        env = {"DOCKER_TLS_VERIFY": "1", "DOCKER_HOST": "tcp://192.168.99.100:2376",
               "DOCKER_CERT_PATH": "C:\Users\Pieter-Jan\.docker\machine\machines\default",
               "DOCKER_MACHINE_NAME": "default", "COMPOSE_CONVERT_WINDOWS_PATHS": "true"}
        client = docker.from_env(environment=env)

        framework_package = locate_framework(self.field_dock.current_release.packages)
        package_folder = framework_package.name + framework_package.version

        try:
            container = client.containers.get("fieldcontainer")
            container.start()
        except docker.errors.NotFound:
            print("MAINGUI -- Container not found, maybe you should install a framework?")

        script_location = "/usr/test/" + package_folder + "/meta/start_script.py"
        command = "python " + script_location
        container.start()
        exe_start = container.exec_run(command, stream=True)
        for val in exe_start:
            print (val)

    def manage_packages(self, event):
        # TODO
        print("Manage installed packages")

    def handle_message(self, event):
        # TODO
        print("Handle messages")

    def install_release(self, event):
        # TODO
        print("Install release")
