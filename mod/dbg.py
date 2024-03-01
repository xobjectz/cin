# This file is in the Public Domain.
#
#

from .obj import fmt


def dbg(event):
    raise Exception(fmt(event))
