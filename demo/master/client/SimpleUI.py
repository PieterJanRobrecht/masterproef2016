#!/usr/bin/env python
# -*- coding: CP1252 -*-
#
# generated by wxGlade 0.7.2 on Tue Feb 21 18:58:45 2017
#

import wx

# begin wxGlade: dependencies
import gettext


# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        wx.Frame.__init__(self, *args, **kwds)
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_1 = wx.StaticText(self, wx.ID_ANY, _("label_1"))
        self.button_1 = wx.Button(self, wx.ID_ANY, _("button_1"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("frame_1"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("sizer_1")), wx.VERTICAL)
        sizer_1.Add(self.text_ctrl_1, 0, 0, 0)
        sizer_1.Add(self.label_1, 0, 0, 0)
        sizer_1.Add(self.button_1, 0, 0, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade


# end of class MyFrame
class MyApp(wx.App):
    def OnInit(self):
        frame_1 = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return True


# end of class MyApp

if __name__ == "__main__":
    gettext.install("app")  # replace with the appropriate catalog name

    app = MyApp(0)
    app.MainLoop()
