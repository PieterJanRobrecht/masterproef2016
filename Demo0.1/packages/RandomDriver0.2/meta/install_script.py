import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../data/opt.py')
# Using python2.7 because of the image
os.system("python2.7 " + str(filename))