import time


class Package(object):
    def __init__(self):
        self.name = None
        self.version = None
        self.description = None
        self.type = None
        self.priority = None
        self.release = time.strftime('%Y-%m-%d')
        self.optional = None
        self.is_framework = None

    def __str__(self):
        keys = ("name", "version", "description", "type", "priority", "release_date", "optional", "is_framework")
        values = (self.name, self.version, self.description, self.type,
                  self.priority, self.release, self.optional, self.is_framework)
        d = dict(zip(keys, values))
        return str(d)

    @classmethod
    def to_tuple(cls, package):
        string = (package.name, package.version, package.description, package.type,
                  package.priority, package.release, package.optional, package.is_framework)
        return string
