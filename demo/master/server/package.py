class Package(object):
    def __init__(self):
        self.id_package = None
        self.name = None
        self.version = None
        self.description = None
        self.location = None
        self.type = None
        self.priority = None
        self.release = None
        self.optional = None
        self.is_framework = None

    def __str__(self):
        keys = ("name", "version", "description", "location", "type", "priority", "release_date", "optional", "is_framework")
        values = (self.name, self.version, self.description, self.location, self.type,
                  self.priority, self.release, self.optional, self.is_framework)
        d = dict(zip(keys, values))
        return str(d)

    @classmethod
    def to_tuple(cls, package):
        string = (package.name, package.version, package.description, package.location, package.type,
                  package.priority, package.release, package.optional, package.is_framework)
        return string

    @classmethod
    def convert_to_package(cls, row):
        p = Package()
        p.id_package = row["idPackage"]
        p.name = row["name"]
        p.version = row["version"]
        p.description = row["description"]
        p.location = row["location"]
        p.type = row["type"]
        p.priority = row["priority"]
        p.release = row["releaseDate"]
        p.optional = row["optional"]
        p.is_framework = row["framework"]
        return p
