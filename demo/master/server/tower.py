import ast
import json

from server.component import Component


class Tower(object):
    def __init__(self):
        self.name = None
        self.serial_number = None
        self.id_in_company = None
        self.location = None
        self.alias = None
        self.components = []

    def __str__(self):
        keys = ("name", "serial_number", "id_in_company", "location", "alias", "components")
        strings = []
        for component in self.components:
            strings.append(str(component))
        values = (self.name, self.serial_number, self.id_in_company, self.location, self.alias, strings)
        d = dict(zip(keys, values))
        return json.dumps(d)

    @classmethod
    def convert_to_tower(cls, data):
        if type(data) is not dict:
            d = ast.literal_eval(data)
        else:
            d = data

        tower = Tower()
        components = d["components"]
        for component in components:
            component = Component.convert_to_component(component)
            tower.components.append(component)
        tower.name = d["name"]
        tower.alias = d["alias"]
        tower.location = d["location"]
        tower.serial_number = d["serial_number"]
        tower.id_in_company = d["id_in_company"]
        return tower

    @classmethod
    def to_tuple(cls, tower):
        string = (tower.name, tower.alias, tower.location, tower.id_in_company, tower.serial_number)
        return string
