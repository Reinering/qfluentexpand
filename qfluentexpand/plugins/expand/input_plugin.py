#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from qfluentexpand.components.line.editor import LineEditor
from base import PluginBase



class Basic_InputPlugin(PluginBase):

    def icon(self):
        return super().icon('TextBox')

    def group(self):
        return super().group() + ' (Basic Input)'


class LineEditorPlugin(Basic_InputPlugin):
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
