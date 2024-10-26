#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtGui import QIcon
import os

from qfluentwidgets import getIconColor, Theme, qconfig

from .base import GoogleMaterialIconBase
from .manager import QFluentManager


class QFluentIcon():

    @classmethod
    def googleIcon(cls, name, theme=Theme.AUTO):
        try:
            name = name.upper()
            GoogleMaterialIconBase.get(name)

            theme = qconfig.theme if theme == Theme.AUTO else theme
            print("mark", os.path.join(QFluentManager.google.getIconPath(), f"{name.lower()}_{getIconColor(theme, reverse=True)}_{QFluentManager.google.size}.svg"))
            print("mark", os.path.exists(os.path.join(QFluentManager.google.getIconPath(), f"{name.lower()}_{getIconColor(theme, reverse=True)}_{QFluentManager.google.size}.svg")))
            if os.path.exists(os.path.join(QFluentManager.google.getIconPath(), f"{name.lower()}_{getIconColor(theme, reverse=True)}_{QFluentManager.google.size}.svg")):
                return getattr(GoogleMaterialIconBase, name)
            else:
                QFluentManager.google.download(name.lower())
                return QIcon()
        except AttributeError as e:
            print(e)
            QFluentManager.google.download(name.lower())
            return QIcon()

