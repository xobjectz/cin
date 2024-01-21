# This file is placed in the Public Domain.


"test imports"


import os, sys


NAME = "zelf"
sys.path.insert(0, os.path.join(os.getcwd(), "..", NAME))
print(sys.path)