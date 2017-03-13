import os
import zipfile

import docker

from server.agent import Agent
from subprocess import Popen, PIPE


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return root


class InstallAgent(Agent):
    def __init__(self):
        super(InstallAgent, self).__init__()

    def action(self):
        print("INSTALL AGENT -- Starting")
        # Unzip folder
        self.unzip()
        # Make new docker container
        dockerfile = find("Dockerfile", self.release_zip_location)
        client = docker.from_env()
        client.containers.run("ubuntu", "echo hello world")
        docker_image = client.images.build(path=dockerfile)
        container = client.containers.create_container("fielddockimage", name="fielddockcontainer")
        # client.start(container)
        # Popen(["docker-machine", "env", "--shell", "cmd", "default"])
        # Popen(["docker", "build", "-t", "fielddock", dockerfile])
        # Popen(["docker", "run", "--name", "fielddockcontainer", "-it", "fielddock"])
        print("INSTALL AGENT -- Docker container created")
        # Copy files to container
        # Locate installer meta file
        # Install all the packages

    def unzip(self):
        release_zip = os.path.join(self.release_zip_location, "release.zip")
        zip_ref = zipfile.ZipFile(release_zip, 'r')
        zip_ref.extractall(self.release_zip_location)
        zip_ref.close()
