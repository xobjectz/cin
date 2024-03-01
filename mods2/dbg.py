# This file is in the Public Domain.
#
#

from cin.objects import fmt


def dbg(event):
    raise Exception(fmt(event))
