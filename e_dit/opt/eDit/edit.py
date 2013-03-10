#!/usr/bin/env python
# encoding: utf-8
import os
import elementary as elm
from launchers import Launchers

"""eDit

An lxde/e17 menu-editor GUI built on Python-EFL's.
By: AntCer (bodhidocs@gmail.com)

Started: March 4, 2013
"""

#---Start

if __name__ == "__main__":
    elm.init()

    Launchers(None)

    elm.run()
    elm.shutdown()

