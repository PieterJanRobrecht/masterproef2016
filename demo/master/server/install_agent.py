import os
import tarfile
import zipfile

import docker
from agent import Agent
from server.installer import Installer


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return root


def create_zip(package_location):
    with tarfile.open(package_location, "w:gz") as tar:
        tar.add(package_location, arcname=os.path.basename(package_location))
        return tar


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
        docker_image = client.images.build(path=dockerfile, tag="fieldimage")
        self.container = client.containers.run(docker_image, detach=True, name="fieldcontainer")
        print("INSTALL AGENT -- Docker container created")
        # Locate installer meta file
        meta_folder = str(find("metadata_installer.json", self.release_zip_location))
        meta_file = os.path.join(meta_folder, "metadata_installer.json")
        self.installer = Installer.convert_to_installer(open(meta_file, "r"))
        # For every package
        for package in self.installer:
            # Copy package to container
            package_name = package.name + package.version
            tar = create_zip(find(package_name, self.release_zip_location))
            # This path has been added by the Dockerfile
            self.container.put_archive("/usr/test/", tar)
            tar.close()
            # Perform the installation
            self.types[package.type](package_name)
            # TODO: Perform test

    def perform_execute(self):
        # TODO
        print "gello"

    def perform_unzip(self):
        # TODO
        print "hello"

    def unzip(self):
        release_zip = os.path.join(self.release_zip_location, "release.zip")
        zip_ref = zipfile.ZipFile(release_zip, 'r')
        zip_ref.extractall(self.release_zip_location)
        zip_ref.close()
