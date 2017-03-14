import os
import zipfile

import docker
from docker import DockerClient
from subprocess import call
import subprocess

from agent import Agent
from subprocess import Popen, PIPE


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return root


def create_zip(release_zip_location):
    print "hallo"


class InstallAgent(Agent):
    def __init__(self):
        super(InstallAgent, self).__init__()

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
        container = client.containers.run(docker_image, detach=True, name="fieldcontainer")
        print("INSTALL AGENT -- Docker container created")
        # Copy files to container
        tar_zip = create_zip(self.release_zip_location)
        # Locate installer meta file
        # Install all the packages

    def unzip(self):
        release_zip = os.path.join(self.release_zip_location, "release.zip")
        zip_ref = zipfile.ZipFile(release_zip, 'r')
        zip_ref.extractall(self.release_zip_location)
        zip_ref.close()
