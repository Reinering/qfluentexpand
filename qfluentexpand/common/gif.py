#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class FluentGif(Enum):

    LOADING = "loading"
    LOADINGV2 = "loadingv2"
    LOADINGV3 = "loadingv3"
    LOADINGV4 = "loadingv4"
    LOADINGV5 = "loadingv5"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/qfluentexpand/gifs/{theme.value.lower()}/{self.value.lower()}.gif"