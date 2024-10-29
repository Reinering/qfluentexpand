#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author:
email:
"""


from qfluentexpand.icongenie.manager import QFluentManager



# iconify   https://icon-sets.iconify.design/
iconify_icons = [
    ("home", "black", 24),
    ("search", "#2196F3", 32),
]


# simpleicons   https://simpleicons.org/
simpleicons_icons = [
    ("4chan", "black", 24),
    ("adafruit", "#2196F3", 32),
]





iconify = QFluentManager.iconify
# iconify.setLibrary("material-symbols")
iconify.setRootPath("./")
# iconify.setResourcePath(os.path.join(ROOT_PATH, "resource_qfe_rc.py"))
iconify.init()
iconify.downloadBlock = True
iconify.download(iconify_icons)

simpleicons = QFluentManager.simpleicons
simpleicons.setRootPath("./")
simpleicons.init()
iconify.downloadBlock = True
simpleicons.download(simpleicons_icons)