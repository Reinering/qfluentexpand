# coding:utf-8
import traceback
from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

from combox_plugin import *
from navi_plugin import *
from selector_plugin import *



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
