#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtGui import QIcon
import os
import sys

from qfluentwidgets import getIconColor, Theme, qconfig

from .base import GoogleMaterialIconBase
from .manager import QFluentManager


class QFluentIcon():

    @classmethod
    def googleIcon(cls, name, theme=Theme.AUTO):
        try:
            name = name.upper()
            GoogleMaterialIconBase.get(name)

            # 判断是否打包
            if not getattr(sys, 'frozen', False) and not '__compiled__' in globals():
                theme = qconfig.theme if theme == Theme.AUTO else theme
                if os.path.exists(os.path.join(QFluentManager.google.getIconPath(), f"{name.lower()}_{getIconColor(theme, reverse=True)}_{QFluentManager.google.size}.svg")):
                    return getattr(GoogleMaterialIconBase, name)
                else:
                    QFluentManager.google.download(name.lower())
                    return QIcon()

            return getattr(GoogleMaterialIconBase, name)
        except AttributeError as e:
            print(e)
            # 判断是否打包
            if getattr(sys, 'frozen', False) or '__compiled__' in globals():
                QFluentManager.google.download(name.lower())
            return QIcon()

