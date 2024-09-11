#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""

from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

# from qfluentwidgets import NavigationPanel, Pivot

from qfluentexpand.components.navigation.navi_interface import Navigation
from qfluentexpand.components.navigation.navigation_interface import NavigationInterface

from base import PluginBase


class NavigationPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Navigation)'

    def icon(self):
        return super().icon("NavigationView")

    def includeFile(self):
        """"
        package name
        """
        return "qfluentexpand.components.navigation.navigation_interface"


class NaviInterfacePlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Navigation interface plugin """
    
    def createWidget(self, parent):
        return Navigation(parent, True, True)

    def name(self):
        return "Navigation"


class Navi_InterfacePlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Navigation interface plugin """

    def createWidget(self, parent):
        return NavigationInterface(parent, True, True)

    def name(self):
        return "Navigation_Interface"



# class NavigationPanelPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
#     """ Navigation panel plugin """
#
#     def createWidget(self, parent):
#         return NavigationPanel(parent)
#
#     def icon(self):
#         return super().icon("NavigationView")
#
#     def name(self):
#         return "NavigationPanel"
#
#
# class PivotPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
#     """ Navigation panel plugin """
#
#     def createWidget(self, parent):
#         p = Pivot(parent)
#         for i in range(1, 4):
#             p.addItem(f'Item{i}', f'Item{i}', print)
#
#         p.setCurrentItem('Item1')
#         return p
#
#     def icon(self):
#         return super().icon("Pivot")
#
#     def name(self):
#         return "Pivot"
