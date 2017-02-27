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
