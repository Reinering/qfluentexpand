#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""



from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from qfluentexpand.components.line.selector import FilePathSelector, FolderPathSelector

from base import PluginBase



class SelectorPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Selector)'

    def icon(self):
        return super().icon("DropDownButton")


class FilePathSelectorPlugin(SelectorPlugin, QDesignerCustomWidgetInterface):

    def createWidget(self, parent):
        return FilePathSelector(parent)

    def name(self):
        return "FilePathSelector"

    def includeFile(self):
        return "qfluentexpand.components.line.selector"


class FolderPathSelectorPlugin(SelectorPlugin, QDesignerCustomWidgetInterface):

    def createWidget(self, parent):
        return FolderPathSelector(parent)

    def name(self):
        return "FolderPathSelector"

    def includeFile(self):
        return "qfluentexpand.components.line.selector"