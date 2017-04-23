import ast
import json

from package import Package


class Installer(object):
    def __init__(self):
        self.id_installer = None
        self.name = None
        self.version = None
        self.disk_location = None
        self.packages = []
        self.new = False

    def __str__(self):
        keys = ("idInstaller", "name", "installerVersion", "diskLocation", "packages")
        strings = []
        for package in self.packages:
            strings.append(str(package))
        values = (self.id_installer, self.name, self.version, self.disk_location, strings)
        d = dict(zip(keys, values))
        return json.dumps(d)

    @classmethod
    def to_tuple(cls, installer):
        string = (installer.name, installer.version, installer.disk_location)
        return string

    @classmethod
    def convert_to_installer(cls, message_data):
        """
            Map the component variables with the database
        :param message_data:
        :return:
        """
        if type(message_data) is not dict:
            d = ast.literal_eval(message_data)
        else:
            d = message_data

        installer = Installer()
        installer.id_installer = d["idInstaller"]
        if "packages" in d:
            packages = d["packages"]
            for package in packages:
                package = Package.convert_to_package(package)
                installer.packages.append(package)
        installer.name = d["name"]
        installer.disk_location = d["diskLocation"]
        installer.version = d["installerVersion"]
        return installer
