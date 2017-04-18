import docker
import docker.errors
import os
import requests.exceptions


class Agent(object):
    def __init__(self):
        self.field_dock = None
        # Information about installer
        self.installer = None
        self.release_zip_location = None
        # Attributes used for docker
        self.client = None
        self.container = None
        self.docker_image = None

    def create_image(self):
        """
            Create Docker image from Dockerfile
        :return:
        """
        dockerfile = str(self.find("Dockerfile", self.release_zip_location))
        self.docker_image = self.client.images.build(path=dockerfile, tag="fieldimage", rm=True)

    def rename_container(self, old_name, new_name):
        """
            Rename container
            If container with new_name already exists
            If so remove it
        :param old_name:
        :param new_name:
        :return:
        """
        try:
            old_container = self.client.containers.get(old_name)
            old_container.rename(new_name)
            old_container.stop()
        except requests.exceptions.Timeout:
            print("AGENT -- Timeout error")
        except docker.errors.NotFound:
            print("AGENT -- Container " + old_name + " does not exist yet")
        except docker.errors.APIError:
            # new_name most likely already exists
            # Time to remove it
            print("AGENT -- API error: removing container with name " + new_name)
            container = self.client.containers.get(new_name)
            container.stop()
            container.remove()
            old_container.rename(new_name)

    def remove_broken_container(self, broken_name):
        """
            Not used
        :param broken_name:
        :return:
        """
        try:
            broken = self.client.containers.get(broken_name)
            broken.stop()
            broken.remove()
        except docker.errors.NotFound:
            print("AGENT -- No container with name " + broken_name + " found")

    def action(self, client):
        """
            Should always be overwritten
        :param client:
        :return:
        """
        print("AGENT -- Performing random action")

    def init_client(self, client):
        self.client = client

    def find(self, name, path):
        """
            Find a filename in a file path
        :param name:
        :param path:
        :return:
        """
        for root, dirs, files in os.walk(path):
            if name in files or name in dirs:
                return root
