# importing wx files
import wx

# import the newly created GUI file
import noname

# importing * : to enable writing sin(13) instead of math.sin(13)
from math import *


# inherit from the MainFrame created in wxFowmBuilder and create CalcFrame
class CalcFrame(noname.MyFrame1):
    # constructor
    def __init__(self, parent):
        # initialize parent class
        noname.MyFrame1.__init__(self, parent)

# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details
app = wx.App(False)

# create an object of CalcFrame
frame = CalcFrame(None)
# show the frame
frame.Show(True)
# start the applications
app.MainLoop()
