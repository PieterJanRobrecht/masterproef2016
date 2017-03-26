import os
import tarfile
import zipfile

from agent import Agent
from server.installer import Installer


def create_zip(package_location):
    new_tar = os.path.join(package_location, "package_tar.tar")
    with tarfile.open(new_tar, "w") as tar:
        tar.add(package_location, arcname=os.path.basename(package_location))
    tar_file = open(new_tar, "rb")
    return tar_file


def has_include(package_name, release_zip_location):
    name = package_name + "/incl"
    for root, dirs, files in os.walk(release_zip_location):
        if name in files or name in dirs:
            return True
        else:
            return False


class InstallAgent(Agent):
    def __init__(self):
        super(InstallAgent, self).__init__()
        self.types = {
            "Executable": self.perform_execute,
            "Zip": self.perform_unzip
        }

    def action(self):
        print("INSTALL AGENT -- Starting")
        # Unzip folder
        self.unzip()
        # Make new docker container
        self.init_client()
        self.create_image()
        # Check if container exists if so rename it
        self.rename_container("fieldcontainer", "old_container")

        self.client.containers.create(self.docker_image, entrypoint="/bin/bash", tty=True, name="fieldcontainer")
        for container in self.client.containers.list(all=True):
            if container.name == "fieldcontainer":
                self.container = container

        print("INSTALL AGENT -- Docker container created")
        # Locate installer meta file
        meta_folder = str(self.find("metadata_installer.json", self.release_zip_location))
        meta_file = os.path.join(meta_folder, "metadata_installer.json")
        self.installer = Installer.convert_to_installer(open(meta_file, "r").read())

        # For every package
        self.installer.packages.sort(key=lambda x: x.priority, reverse=True)
        non_optional_packages = (package for package in self.installer.packages if not package.optional)

        # First install necessary packages
        for package in non_optional_packages:
            self.install_package(self.client, package)
            # TODO: Perform test

        # Install all the other packages
        optional_packages = (package for package in self.installer.packages if package.optional)
        for package in optional_packages:
            self.install_package(self.client, package)
            # TODO: Perform test

        # If all test are successful
        success = True
        if success:
            print("INSTALL AGENT -- Finished")
            self.send_update()
        else:
            print("INSTALL AGENT -- Not all tests finished correctly, rolling back to previous state")
            self.rollback()

    def perform_execute(self, client, package_name, has_include_folder):
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
        release_zip = os.path.join(self.release_zip_location, "release.zip")
        zip_ref = zipfile.ZipFile(release_zip, 'r')
        zip_ref.extractall(self.release_zip_location)
        zip_ref.close()

    def install_package(self, client, package):
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

    def rollback(self):
        self.remove_broken_container("fieldcontainer")
        self.rename_container("old_container", "fieldcontainer")

    def send_update(self):
        self.field_dock.update_info_installer(self.installer)
