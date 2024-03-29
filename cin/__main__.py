#!/usr/bin/env python3
# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0201,W0212,W0613,E0402,E0611
# ruff: noqa: E402


"""CIN - central intelligence name

SYNOPSIS

    cin <cmd> [key=val] [key==val]
    cin [-a] [-c] [-d] [-h] [-v]

COMMANDS

    cmd    list available commands
    mod    list available modules

OPTIONS

    -a     load all modules
    -c     start console
    -d     start daemon
    -h     display help
    -v     use verbose
"""


import getpass
import os
import pwd
import readline
import sys
import termios
import time


from obj import Default
from pst import Workdir
from run import Client, Errors, Event, listmods
from run import cmnd, debug, forever, init, parse_cmd, scan


from cin import mod as mods


Cfg         = Default()
Cfg.mod     = "cmd,mod"
Cfg.name    = "cin"
Cfg.modpath = os.path.expanduser("~/mods")
Cfg.version = "110"
Cfg.wd      = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wd, f"{Cfg.name}.pid")


Workdir.wd = Cfg.wd


dte = time.ctime(time.time()).replace("  ", " ")


class Console(Client):

    def announce(self, txt):
        pass

    def callback(self, evt):
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Event()
        evt.orig = object.__repr__(self)
        evt.txt = input("> ")
        evt.type = "command"
        return evt

    def say(self, channel, txt):
        txt = txt.encode('utf-8', 'replace').decode()
        print(txt)


def daemon(pidfile, verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    Workdir.cdir(os.path.dirname(pidfile))
    with open(pidfile, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges(username):
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def wrap(func):
    old2 = None
    try:
        old2 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old2:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old2)


def main():
    Errors.enable(print)
    Workdir.skel()
    parse_cmd(Cfg, " ".join(sys.argv[1:]))
    readline.redisplay()
    if 'a' in Cfg.opts:
        Cfg.mod = ",".join(listmods(Cfg.modpath))
    if "v" in Cfg.opts:
        debug(f"{Cfg.name.upper()} {Cfg.opts.upper()} started {dte}")
    if "h" in Cfg.opts:
        print(__doc__)
        return
    if "d" in Cfg.opts:
        Cfg.mod = ",".join(mods.__dir__())
        Cfg.user = getpass.getuser()
        daemon(Cfg.pidfile, "v" in Cfg.opts)
        privileges(Cfg.user)
        scan(mods, Cfg.mod, Cfg.sets.dis)
        init(mods, Cfg.mod, Cfg.sets.dis)
        forever()
        return
    if "c" in Cfg.opts:
        scan(mods, Cfg.mod, Cfg.sets.dis)
        init(mods, Cfg.mod, Cfg.sets.dis)
        csl = Console()
        csl.start()
        forever()
        return
    if Cfg.otxt:
        Cfg.mod = ",".join(mods.__dir__())
        scan(mods, Cfg.mod, Cfg.sets.dis)
        return cmnd(Cfg.otxt, print)


def wrapped():
    wrap(main)
    Errors.show()


if __name__ == "__main__":
    wrapped()
