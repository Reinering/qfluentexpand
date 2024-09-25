#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtDesigner import (QDesignerCustomWidgetInterface, QDesignerFormWindowInterface, QExtensionFactory,
                              QPyDesignerContainerExtension)
from qfluentwidgets import (ExpandGroupSettingCard)

from plugin_base import PluginBase


class CardPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Card)'

    def icon(self):
        return super().icon("CommandBar")

    def isContainer(self):
        return True


class CardWidgetPlugin(CardPlugin, QDesignerCustomWidgetInterface):
    """ Card plugin """

    def createWidget(self, parent):
        return ExpandGroupSettingCard(parent)

    def name(self):
        return "ExpandGroupSettingCard"