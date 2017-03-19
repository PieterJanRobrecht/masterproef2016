import os
import tarfile
import zipfile

import docker

from agent import Agent
from server.installer import Installer


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files or name in dirs:
            return root


def create_zip(package_location):
    new_tar = os.path.join(package_location, "package_tar.tar")
    with tarfile.open(new_tar, "w") as tar:
        tar.add(package_location, arcname=os.path.basename(package_location))
    tar_file = open(new_tar, "rb")
    return tar_file


class InstallAgent(Agent):

    def __init__(self):
        super(InstallAgent, self).__init__()
        self.installer = None
        self.container = None
        self.types = {
            "Executable": self.perform_execute,
            "Zip": self.perform_unzip
        }

    def action(self):
        print("INSTALL AGENT -- Starting")
        # Unzip folder
        self.unzip()
        # Make new docker container
        dockerfile = str(find("Dockerfile", self.release_zip_location))
        env = {"DOCKER_TLS_VERIFY": "1", "DOCKER_HOST": "tcp://192.168.99.100:2376",
               "DOCKER_CERT_PATH": "C:\Users\Pieter-Jan\.docker\machine\machines\default",
               "DOCKER_MACHINE_NAME": "default", "COMPOSE_CONVERT_WINDOWS_PATHS": "true"}
        client = docker.from_env(environment=env)
        docker_image = client.images.build(path=dockerfile, tag="fieldimage", rm=True)
        # Check if container exists if so rename it
        # try:
        #     old_container = client.containers.get("fieldcontainer")
        #     old_container.rename("old_container")
        # except:
        #     print("INSTALL AGENT -- Fieldcontainer does not exist")
        # finally:
        # self.container = client.containers.run(docker_image, detach=True, name="fieldcontainer")
        client.containers.create(docker_image, entrypoint="/bin/bash", tty=True, name="fieldcontainer")
        for container in client.containers.list(all=True):
            if container.name == "fieldcontainer":
                self.container = container

        print("INSTALL AGENT -- Docker container created")
        # Locate installer meta file
        meta_folder = str(find("metadata_installer.json", self.release_zip_location))
        meta_file = os.path.join(meta_folder, "metadata_installer.json")
        self.installer = Installer.convert_to_installer(open(meta_file, "r").read())
        # For every package
        for package in self.installer.packages:
            # Copy package to container
            package_name = package.name + package.version
            package_location = find(package_name, self.release_zip_location)
            tar = create_zip(str(os.path.join(package_location, package_name)))
            # This path has been added by the Dockerfile
            self.container.put_archive("/usr/test/", tar)
            tar.close()
            # Perform the installation
            self.types[package.type](client, package_name)
            # TODO: Perform test
        # If all test are successful
        success = True
        if success:
            print("INSTALL AGENT -- Finished")
        #     old_container.stop()
        #     old_container.remove()
        # else:
        #     self.container.stop()
        #     self.container.remove()
        #     old_container.rename("fieldcontainer")
        #     self.container = old_container

    def perform_execute(self, client, package_name):
        print("INSTALL AGENT -- Performing action: EXECUTE")
        script_location = "/usr/test/" + package_name + "/meta/install_script.py"
        command = "python " + script_location
        self.container.start()
        exe_start = self.container.exec_run(command, stream=True)
        for val in exe_start:
            print (val)
        print("INSTALL AGENT -- Done with: EXECUTE")

    def perform_unzip(self, client, package_name):
        # TODO
        print "hello"

    def unzip(self):
        release_zip = os.path.join(self.release_zip_location, "release.zip")
        zip_ref = zipfile.ZipFile(release_zip, 'r')
        zip_ref.extractall(self.release_zip_location)
        zip_ref.close()
