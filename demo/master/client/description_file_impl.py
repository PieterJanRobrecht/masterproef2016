import description_file_gui

from server.component import Component
from server.tower import Tower


class DescriptionCreator(description_file_gui.MyFrame2):
    def __init__(self, parent):
        """
            Implementation of the description_file_gui file
            Handles all actions performed by the GUI
        :param parent:
        """
        description_file_gui.MyFrame2.__init__(self, parent)
        self.root = self.tree_control.AddRoot("Tower")
        self.tower = Tower()

    def component_submit(self, event):
        """
            Add component to Tower
        :param event:
        """
        component = Component()
        component.manufacturer = str(self.manufacturer_text.GetValue())
        component.product_number = str(self.product_number_text.GetValue())
        component.calibration_number = str(self.calibration_number_text.GetValue())
        component.serial_number = str(self.serial_number_component_text.GetValue())
        component.firmware_version = str(self.firmware_text.GetValue())

        self.tower.components.append(component)
        self.add_to_tree(component)
        event.Skip()

    def component_clear(self, event):
        """
            Clear all the fields belonging to component
        :param event:
        """
        self.manufacturer_text.SetValue("")
        self.product_number_text.SetValue("")
        self.calibration_number_text.SetValue("")
        self.serial_number_component_text.SetValue("")
        self.firmware_text.SetValue("")
        event.Skip()

    def tower_submit(self, event):
        """
            Take text from fields
            Save tower configuration to file
        :param event:
        """
        self.tower.name = str(self.tower_name_text.GetValue())
        self.tower.alias = str(self.tower_alias_text.GetValue())
        self.tower.id_in_company = str(self.id_tower_text.GetValue())
        self.tower.location = str(self.location_text.GetValue())
        self.tower.serial_number = str(self.serial_number_tower_text.GetValue())
        self.tower.id_tower = -1
        self.tower.id_installer = -1
        self.write_to_file()
        event.Skip()
        self.Close()

    def tower_clear(self, event):
        """
            Clear all the fields belonging to tower
        :param event:
        """
        self.tower_name_text.SetValue("")
        self.serial_number_tower_text.SetValue("")
        self.id_tower_text.SetValue("")
        self.location_text.SetValue("")
        self.tower_alias_text.SetValue("")
        event.Skip()

    def add_to_tree(self, component):
        """
            Add a component to the tree_view
        :param component:
        """
        tree = self.tree_control
        manu = "Manufacturer: " + component.manufacturer
        cal = "Calibration: " + component.calibration_number
        prod = "Product Number: " + component.product_number
        firm = "Firmware: " + component.firmware_version
        text = "Component: " + component.serial_number
        comp = tree.AppendItem(self.root, text)

        tree.AppendItem(comp, manu)
        tree.AppendItem(comp, cal)
        tree.AppendItem(comp, prod)
        tree.AppendItem(comp, firm)

    def write_to_file(self):
        """
            Write tower to file description_file.json
            If the file not exists, create it
        """
        file_name = "description_file.json"
        description_file = open(file_name, 'w+')
        description_file.write(str(self.tower))
