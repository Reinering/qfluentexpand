#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from fluent_widgets.components.combox.combo_box import MSEComboBox
from basic_input import BasicInputPlugin



class MSEComboBoxPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Combo box plugin """

    def createWidget(self, parent):
        return MSEComboBox(parent)

    def icon(self):
        return super().icon('ComboBox')

    def name(self):
        return "MSEComboBox"

    def includeFile(self):
        """"
        package name
        """
        return "qfluentexpand.components.combox.combo_box.MSEComboBox"