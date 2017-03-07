import ast

from package import Package


class Installer(object):
    def __init__(self):
        self.name = None
        self.version = None
        self.disk_location = None
        self.packages = []

    def __str__(self):
        keys = ("name", "version", "disk_location", "packages")
        strings = []
        for package in self.packages:
            strings.append(str(package))
        values = (self.name, self.version, self.disk_location, strings)
        d = dict(zip(keys, values))
        return str(d)

    @classmethod
    def to_tuple(cls, installer):
        string = (installer.name, installer.version, installer.disk_location)
        return string

    @classmethod
    def convert_to_tower(cls, message_data):
        if type(message_data) is not dict:
            d = ast.literal_eval(message_data)
        else:
            d = message_data

        installer = Installer()
        packages = d["packages"]
        for package in packages:
            package = Package.convert_to_package(package)
            installer.packages.append(package)
        installer.name = d["name"]
        installer.disk_location = d["disk_location"]
        installer.version = d["version"]
        return installer
