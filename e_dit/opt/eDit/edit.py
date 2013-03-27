#!/usr/bin/env python
# encoding: utf-8
import os
import elementary as elm
from ecore import Exe
from launchers import Launchers
from time import sleep

"""eDit

A menu-editor GUI built on Python-EFL's.
By: AntCer (bodhidocs@gmail.com)

Started: March 4, 2013
"""
HOME = os.getenv("HOME")
CONFIG = "%s/.config/eDit/"%HOME
DIR = "%s/.local/share/desktop-directories/" %HOME
MENU = "%s/.config/menus/" %HOME



#---Config Files
if not os.path.isdir(MENU):
    Exe("mkdir '%s'"%MENU)
    sleep(2)
if not os.path.isdir(DIR):
    Exe("mkdir '%s'"%DIR)
    sleep(2)
if not os.path.isdir(CONFIG):
    Exe("mkdir '%s'"%CONFIG)
    sleep(10)
if not os.path.exists("%sdefault.view"%CONFIG):
    Exe("echo 'catview=False' > '%sdefault.view'"%CONFIG)
    sleep(10)

#---Start

if __name__ == "__main__":
    elm.init()

    Launchers(None)

    elm.run()
    elm.shutdown()

