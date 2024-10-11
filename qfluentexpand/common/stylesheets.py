#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class STYLESHEET(StyleSheetBase, Enum):
    """ Style sheet  """

    EXPAND_CARD = "expand_card"


    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/qfluentexpand/qss/{theme.value.lower()}/{self.value.lower()}.qss"