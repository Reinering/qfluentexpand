#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from qfluentexpand.components.line.editor import LineEditor
from base import PluginBase



class InputPlugin(PluginBase):

    def icon(self):
        return super().icon('TextBox')

    def group(self):
        return super().group() + ' (Input)'


class LineEditorPlugin(InputPlugin, QDesignerCustomWidgetInterface):
    """ Line editor plugin """

    def createWidget(self, parent):
        return LineEditor(parent)

    def name(self):
        return "LineEditor"

    def includeFile(self):
        """"
        package name
        """
        return "qfluentexpand.components.line.editor"
