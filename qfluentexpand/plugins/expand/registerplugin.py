#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

from input_plugin import *
from combox_plugin import *
from navi_plugin import *
from selector_plugin import *


# input_plugin
QPyDesignerCustomWidgetCollection.addCustomWidget(LineEditorPlugin())

# combox_plugin
QPyDesignerCustomWidgetCollection.addCustomWidget(MSComboBoxPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(MSEComboBoxPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(MSECComboBoxPlugin())

# navi_plugin
QPyDesignerCustomWidgetCollection.addCustomWidget(NaviInterfacePlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(Navi_InterfacePlugin())

# selector_plugin
QPyDesignerCustomWidgetCollection.addCustomWidget(FilePathSelectorPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(FolderPathSelectorPlugin())
