import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../data/demo_gui_1.py')
# Using python2.7 because of the image

os.system("python2.7 " + str(filename))