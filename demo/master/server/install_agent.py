import os
import tarfile
import zipfile
import time

from agent import Agent
from installer import Installer
from message import Message


def create_zip(package_location):
    """
        Create a zip file on the given location
    :param package_location:
    :return:
    """
    new_tar = os.path.join(package_location, "package_tar.tar")
    with tarfile.open(new_tar, "w") as tar:
        tar.add(package_location, arcname=os.path.basename(package_location))
    tar_file = open(new_tar, "rb")
    return tar_file


def has_include(package_name, release_zip_location):
    """
        Check if package has include folder
    :param package_name:
    :param release_zip_location:
    :return:
    """
    name = package_name + "/incl"
    for root, dirs, files in os.walk(release_zip_location):
        if name in files or name in dirs:
            return True
        else:
            return False


class InstallAgent(Agent):
    def __init__(self):
        super(InstallAgent, self).__init__()
        self.old_installer = None
        self.types = {
            "Executable": self.perform_execute,
            "Zip": self.perform_unzip
        }

    def action(self, client):
        """
            Rename the fieldconta   iner
            Create new container
            Send update to broker
            Get meta_data file
            For every package install
            If fail quarantine container and send new update
        :param client:
        :return:
        """
        print("INSTALL AGENT -- Starting")
        # Unzip folder
        self.unzip()
        # Make new docker container
        self.init_client(client)
        self.create_image()
        # Check if container exists if so rename it
        self.rename_container("fieldcontainer", "old_container")
        # Parameters to pass on the X11 display
        self.client.containers.create(self.docker_image, entrypoint="/bin/bash", tty=True, name="fieldcontainer",
                                      # environment=["DISPLAY=192.168.1.4:0.0"])
                                      environment=["DISPLAY=10.2.0.72:0.0"])
        for container in self.client.containers.list(all=True):
            if container.name == "fieldcontainer":
                self.container = container

        print("INSTALL AGENT -- Docker container created")
        # Locate installer meta file
        meta_folder = str(self.find("metadata_installer.json", self.release_zip_location))
        meta_file = os.path.join(meta_folder, "metadata_installer.json")
        self.old_installer = self.installer
        self.installer = Installer.convert_to_installer(open(meta_file, "r").read())

        self.send_update()

        # For every package
        self.installer.packages.sort(key=lambda x: x.priority, reverse=True)
        non_optional_packages = (package for package in self.installer.packages if not package.optional)

        success = True
        # First install necessary packages
        for package in non_optional_packages:
            self.install_package(self.client, package)
            if not self.check_installation(self.client, package):
                success = False
                print("INSTALL AGENT -- Test failed, container will be quarantined in the end")

        # Install framework
        framework_packages = (package for package in self.installer.packages if package.is_framework)
        for package in framework_packages:
            self.install_package(self.client, package)
            if not self.check_installation(self.client, package):
                success = False
                print("INSTALL AGENT -- Test failed, container will be quarantined in the end")

        # Install all the other packages
        optional_packages = (package for package in self.installer.packages if package.optional)
        for package in optional_packages:
            self.install_package(self.client, package)
            if not self.check_installation(self.client, package):
                success = False
                print("INSTALL AGENT -- Test failed, container will be quarantined in the end")

        # If all test are successful
        if success:
            print("INSTALL AGENT -- Finished with installation")
        else:
            print("INSTALL AGENT -- Not all tests finished correctly, rolling back to previous state")
            self.installer = self.old_installer
            self.send_update()
            self.quarantine()
        self.field_dock.kill_containers()

    def perform_execute(self, client, package_name, has_include_folder):
        """
            Locate install script in container
            Execute command in container
        :param client:
        :param package_name:
        :param has_include_folder:
        :return:
        """
        print("INSTALL AGENT -- Performing action: EXECUTE")
        script_location = "/usr/test/" + package_name + "/meta/install_script.py"
        command = "python " + script_location
        self.container.start()
        exe_start = self.container.exec_run(command, stream=True)
        for val in exe_start:
            print (val)
        if has_include_folder:
            # TODO: handle include folder
            print("TODO has include")
        print("INSTALL AGENT -- Done with: EXECUTE")

    def perform_unzip(self, client, package_name, has_include):
        # TODO
        print "hello"

    def unzip(self):
        """
            Unzip release zip
        :return:
        """
        release_zip = os.path.join(self.release_zip_location, "release.zip")
        zip_ref = zipfile.ZipFile(release_zip, 'r')
        zip_ref.extractall(self.release_zip_location)
        zip_ref.close()

    def install_package(self, client, package):
        """
            Copy package to container
            Perform installation of package
        :param client:
        :param package:
        :return:
        """
        # Copy package to container
        package_name = package.name + package.version
        package_location = self.find(package_name, self.release_zip_location)
        has_include_folder = has_include(package_name, self.release_zip_location)
        tar = create_zip(str(os.path.join(package_location, package_name)))
        # This path has been added by the Dockerfile
        self.container.put_archive("/usr/test/", tar)
        tar.close()
        # Perform the installation
        self.types[package.type](client, package_name, has_include_folder)

    def quarantine(self):
        """
            Rename fieldcontainer to quarantine
            Rename oldcontainer to fieldcontainer
        :return:
        """
        self.rename_container("fieldcontainer", "quarantined")
        self.rename_container("old_container", "fieldcontainer")

    def send_update(self):
        """
            Send update to broker
        :return:
        """
        self.field_dock.update_info_installer(self.installer)

    def check_installation(self, client, package):
        """
            Locate test script in container
            Perform execute in container
            Send rapport to broker
        :param client:
        :param package:
        :return:
        """
        start_time = time.time()
        package_name = package.name + package.version
        script_location = "/usr/test/" + package_name + "/meta/test_script.py"
        command = "python " + script_location
        self.container.start()
        exe_start = self.container.exec_run(command, stream=True)
        for val in exe_start:
            if val.startswith("0"):
                print("INSTALL AGENT -- Package " + package_name + " was correctly installed")
                answer = True
            else:
                print("INSTALL AGENT -- Package " + package_name + " ended with error \n\t ERROR " + val)
                answer = False

        end_time = time.time()
        data = {"start_time": start_time, "end_time": end_time,
                "result": val, "name": package.name, "version": package.version}
        message = Message()
        message.create_message(self.field_dock.host, "rapport", data)
        self.field_dock.send_message(message)
        print("INSTALL AGENT -- Rapport send to release dock")
        return answer
