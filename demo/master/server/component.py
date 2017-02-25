import ast
import json

from data.decorators import data


class Component(object):
    def __init__(self):
        self.manufacturer = None
        self.product_number = None
        self.calibration_number = None
        self.serial_number = None
        self.firmware_version = None

    def __str__(self):
        keys = ("manufacturer", "product_number", "calibration_number", "serial_number", "firmware_version")
        values = (
            self.manufacturer, self.product_number, self.calibration_number, self.serial_number, self.firmware_version)
        d = dict(zip(keys, values))
        return json.dumps(d)

    @classmethod
    def convert_to_component(cls, component):
        if type(component) is not dict:
            d = ast.literal_eval(component)
        else:
            d = component

        component = Component()
        component.manufacturer = d["manufacturer"]
        component.product_number = d["product_number"]
        component.calibration_number = d["calibration_number"]
        component.serial_number = d["serial_number"]
        component.serial_number = d["firmware_version"]
        return component

    @classmethod
    def to_tuple(cls, component):
        return (component.manufacturer, component.product_number, component.calibration_number, component.serial_number,
                component.firmware_version)
