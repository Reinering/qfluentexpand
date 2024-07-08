#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""

from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from qfluentwidgets import NavigationPanel, Pivot

from fluent_widgets.components.navigation.navigation_interface import NavigationInterface

from base import PluginBase


class NavigationPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Navigation)'


class NavigationInterfacePlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Navigation interface plugin """
    
    def createWidget(self, parent):
        return NavigationInterface(parent, True, True)

    def icon(self):
        return super().icon("NavigationView") 

    def name(self):
        return "NavigationInterface"

    def includeFile(self):
        """"
        package name
        """
        return "qfluentexpand.components.navigation.navigation_interface"


class NavigationPanelPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Navigation panel plugin """

    def createWidget(self, parent):
        return NavigationPanel(parent)

    def icon(self):
        return super().icon("NavigationView")

    def name(self):
        return "NavigationPanel"


class PivotPlugin(NavigationPlugin, QDesignerCustomWidgetInterface):
    """ Navigation panel plugin """

    def createWidget(self, parent):
        p = Pivot(parent)
        for i in range(1, 4):
            p.addItem(f'Item{i}', f'Item{i}', print)

        p.setCurrentItem('Item1')
        return p

    def icon(self):
        return super().icon("Pivot")

    def name(self):
        return "Pivot"