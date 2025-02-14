#!/usr/bin/env python
# -*- coding: CP1252 -*-
#
# generated by wxGlade 0.7.2 on Sat Feb 25 10:11:43 2017
#

import wx

# begin wxGlade: dependencies
import gettext

# end wxGlade

# begin wxGlade: extracode
# end wxGlade
from server.component import Component
from server.tower import Tower


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # Custom attributes
        self.tower = None
        self.root = None

        # begin wxGlade: MyFrame.__init__
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Manufacturer"))
        self.manufacturer_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_2 = wx.StaticText(self, wx.ID_ANY, _("Product Number"))
        self.product_number_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_3 = wx.StaticText(self, wx.ID_ANY, _("Calibration Number"))
        self.calibration_number_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_4 = wx.StaticText(self, wx.ID_ANY, _("Serial Number"))
        self.serial_number_component_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_5 = wx.StaticText(self, wx.ID_ANY, _("Firmware Version"))
        self.firmware_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.component_submit_button = wx.Button(self, wx.ID_ANY, _("Submit"))
        self.component_clear_button = wx.Button(self, wx.ID_ANY, _("Clear"))
        self.label_6 = wx.StaticText(self, wx.ID_ANY, _("Name"))
        self.tower_name_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_7 = wx.StaticText(self, wx.ID_ANY, _("Serial Number"))
        self.serial_number_tower_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_8 = wx.StaticText(self, wx.ID_ANY, _("ID In Company"))
        self.id_tower_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_9 = wx.StaticText(self, wx.ID_ANY, _("Geolocation"))
        self.location_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_10 = wx.StaticText(self, wx.ID_ANY, _("Alias"))
        self.tower_alias_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.tower_submit_button = wx.Button(self, wx.ID_ANY, _("Submit"))
        self.tower_clear_button = wx.Button(self, wx.ID_ANY, _("Clear"))
        self.tree_control = wx.TreeCtrl(self, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.component_submit, self.component_submit_button)
        self.Bind(wx.EVT_BUTTON, self.component_clear, self.component_clear_button)
        self.Bind(wx.EVT_BUTTON, self.tower_submit, self.tower_submit_button)
        self.Bind(wx.EVT_BUTTON, self.tower_clear, self.tower_clear_button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("Description File"))
        self.tree_control.SetMinSize((220, 352))
        self.root = self.tree_control.AddRoot("Tower")
        self.tower = Tower()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(1, 2, 0, 0)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.FlexGridSizer(4, 1, 0, 0)
        tower_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_3 = wx.GridSizer(5, 2, 5, 5)
        comonent_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_2 = wx.FlexGridSizer(5, 2, 5, 5)
        grid_sizer_2.Add(self.label_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.manufacturer_text, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.label_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.product_number_text, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.label_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.calibration_number_text, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.label_4, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.serial_number_component_text, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.label_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.firmware_text, 0, wx.EXPAND, 0)
        sizer_2.Add(grid_sizer_2, 1, 0, 0)
        sizer_8.Add(self.component_submit_button, 0, wx.EXPAND, 0)
        comonent_buttons.Add(sizer_8, 1, 0, 0)
        sizer_9.Add(self.component_clear_button, 0, wx.EXPAND, 0)
        comonent_buttons.Add(sizer_9, 1, 0, 0)
        sizer_2.Add(comonent_buttons, 1, 0, 0)
        grid_sizer_3.Add(self.label_6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_3.Add(self.tower_name_text, 0, wx.EXPAND, 0)
        grid_sizer_3.Add(self.label_7, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_3.Add(self.serial_number_tower_text, 0, wx.EXPAND, 0)
        grid_sizer_3.Add(self.label_8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_3.Add(self.id_tower_text, 0, wx.EXPAND, 0)
        grid_sizer_3.Add(self.label_9, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_3.Add(self.location_text, 0, wx.EXPAND, 0)
        grid_sizer_3.Add(self.label_10, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_3.Add(self.tower_alias_text, 0, wx.EXPAND, 0)
        sizer_2.Add(grid_sizer_3, 1, 0, 0)
        sizer_10.Add(self.tower_submit_button, 0, wx.ALIGN_RIGHT | wx.EXPAND, 0)
        tower_buttons.Add(sizer_10, 1, 0, 0)
        sizer_11.Add(self.tower_clear_button, 0, wx.EXPAND, 0)
        tower_buttons.Add(sizer_11, 1, 0, 0)
        sizer_2.Add(tower_buttons, 1, 0, 0)
        grid_sizer_1.Add(sizer_2, 1, wx.ALIGN_CENTER, 0)
        sizer_5.Add(self.tree_control, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_5, 1, 0, 0)
        sizer_1.Add(grid_sizer_1, 1, 0, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def component_submit(self, event):  # wxGlade: MyFrame.<event_handler>
        component = Component()
        component.manufacturer = str(self.manufacturer_text.GetValue())
        component.product_number = str(self.product_number_text.GetValue())
        component.calibration_number = str(self.calibration_number_text.GetValue())
        component.serial_number = str(self.serial_number_component_text.GetValue())
        component.firmware_version = str(self.firmware_text.GetValue())

        self.tower.components.append(component)
        self.add_to_tree(component)
        event.Skip()

    def component_clear(self, event):  # wxGlade: MyFrame.<event_handler>
        self.manufacturer_text.SetValue("")
        self.product_number_text.SetValue("")
        self.calibration_number_text.SetValue("")
        self.serial_number_component_text.SetValue("")
        self.firmware_text.SetValue("")
        event.Skip()

    def tower_submit(self, event):  # wxGlade: MyFrame.<event_handler>
        self.tower.name = str(self.tower_name_text.GetValue())
        self.tower.alias = str(self.tower_alias_text.GetValue())
        self.tower.id_in_company = str(self.id_tower_text.GetValue())
        self.tower.location = str(self.location_text.GetValue())
        self.tower.serial_number = str(self.serial_number_tower_text.GetValue())

        self.write_to_file()
        event.Skip()
        self.Close()

    def tower_clear(self, event):  # wxGlade: MyFrame.<event_handler>
        self.tower_name_text.SetValue("")
        self.serial_number_tower_text.SetValue("")
        self.id_tower_text.SetValue("")
        self.location_text.SetValue("")
        self.tower_alias_text.SetValue("")
        event.Skip()

    def add_to_tree(self, component):
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
        file_name = "description_file.json"
        description_file = open(file_name, 'w+')
        description_file.write(str(self.tower))


# end of class MyFrame
class DescriptionGui(wx.App):
    def OnInit(self):
        frame_1 = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return True
