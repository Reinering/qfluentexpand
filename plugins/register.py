#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

from navi_plugin import NaviInterfacePlugin
from combox_plugin import MSEComboBoxPlugin




QPyDesignerCustomWidgetCollection.addCustomWidget(NaviInterfacePlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(MSEComboBoxPlugin())
