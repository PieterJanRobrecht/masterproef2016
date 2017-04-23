import ast
import json


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
        self.new = False

    def __str__(self):
        keys = ("idPackage", "name", "version", "description", "location", "type",
                "priority", "releaseDate", "optional", "framework")
        values = (self.id_package, self.name, self.version, self.description, self.location, self.type,
                  self.priority, str(self.release), self.optional, self.is_framework)
        d = dict(zip(keys, values))
        return json.dumps(d)

    @classmethod
    def to_tuple(cls, package):
        string = (package.name, package.version, package.description, package.location, package.type,
                  package.priority, package.release, package.optional, package.is_framework)
        return string

    @classmethod
    def convert_to_package(cls, row):
        """
            Map the row variables with the database
        :param row:
        :return:
        """
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

    @classmethod
    def convert_to_package(cls, package):
        if type(package) is not dict:
            d = ast.literal_eval(package)
        else:
            d = package

        package = Package()
        package.id_package = d["idPackage"]
        package.name = d["name"]
        package.version = d["version"]
        package.description = d["description"]
        package.location = d["location"]
        package.type = d["type"]
        package.priority = d["priority"]
        package.release = d["releaseDate"]
        package.optional = d["optional"]
        package.is_framework = d["framework"]
        return package
