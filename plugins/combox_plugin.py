#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from qfluentexpand.components.combox.combo_box import MSEComboBox, MSECComboBox, MSComboBox
from basic_input import BasicInputPlugin
from base import PluginBase



class ComboBoxPlugin(PluginBase):

    def icon(self):
        return super().icon('ComboBox')

    def group(self):
        return super().group() + ' (ComboBox)'

    def includeFile(self):
        """"
        package name
        """
        return "qfluentexpand.components.combox.combo_box"


class MSComboBoxPlugin(ComboBoxPlugin, QDesignerCustomWidgetInterface):
    """ Combo box plugin """

    def createWidget(self, parent):
        return MSComboBox(parent)

    def name(self):
        return "MSComboBox"


class MSEComboBoxPlugin(ComboBoxPlugin, QDesignerCustomWidgetInterface):
    """ Combo box plugin """

    def createWidget(self, parent):
        return MSEComboBox(parent)

    def name(self):
        return "MSEComboBox"


class MSECComboBoxPlugin(ComboBoxPlugin, QDesignerCustomWidgetInterface):
    """ Combo box plugin """

    def createWidget(self, parent):
        return MSECComboBox(parent)

    def name(self):
        return "MSECComboBox"
