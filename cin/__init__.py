# This file is placed in the Public Domain.
#
#


"definition"


import os
import sys


import importlib
import os



dname = os.path.dirname(__file__)

sys.path.insert(0, dname)
sys.path.insert(0, os.path.join(dname, "lib"))
sys.path.insert(0, os.path.join(dname, "mod"))


modules = []


def __dir__():
    return modules


for pth in os.listdir(dname):
    subpath = os.path.join(dname, pth)
    if os.path.isdir(subpath):
        for path in os.listdir(dname):
            if path.startswith("__"):
                continue
            if not path.endswith(".py"):
                continue
            name = path[:-3]
            mod = importlib.import_module(name)
            modules.append(name)


from lib import *
from mod import *