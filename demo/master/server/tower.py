import ast
import json

from component import Component


class Tower(object):
    def __init__(self):
        self.id_tower = None
        self.name = None
        self.serial_number = None
        self.id_in_company = None
        self.location = None
        self.alias = None
        self.components = []

    def __str__(self):
        keys = ("idTower", "name", "serialNumber", "idInCompany", "geolocation", "alias", "components")
        strings = []
        for component in self.components:
            strings.append(str(component))
        values = (self.id_tower, self.name, self.serial_number, self.id_in_company, self.location, self.alias, strings)
        d = dict(zip(keys, values))
        return json.dumps(d)

    @classmethod
    def convert_to_tower(cls, data):
        if type(data) is not dict:
            d = ast.literal_eval(data)
        else:
            d = data

        tower = Tower()
        if "components" in d:
            components = d["components"]
            for component in components:
                component = Component.convert_to_component(component)
                tower.components.append(component)
        tower.name = d["idTower"]
        tower.name = d["name"]
        tower.alias = d["alias"]
        tower.location = d["geolocation"]
        tower.serial_number = d["serialNumber"]
        tower.id_in_company = d["idInCompany"]
        return tower

    @classmethod
    def to_tuple(cls, tower):
        string = (tower.name, tower.alias, tower.location, tower.id_in_company, tower.serial_number)
        return string
