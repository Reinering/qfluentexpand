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

from .base import GoogleMaterialIconBase, IconifyIconBase, SimpleIconsIconBase
from .manager import QFluentManager


class QFluentIcon():

    @classmethod
    def googleIcon(cls, name, theme=Theme.AUTO, reverse=False):
        try:
            name = name.upper()
            GoogleMaterialIconBase.get(name)

            # 判断是否打包
            if not getattr(sys, 'frozen', False) and not '__compiled__' in globals():
                theme = qconfig.theme if theme == Theme.AUTO else theme
                if os.path.exists(os.path.join(QFluentManager.google.getIconPath(), f"{name.lower()}_{getIconColor(theme, reverse=reverse)}_{QFluentManager.google.size}.svg")):
                    return getattr(GoogleMaterialIconBase, name)
                else:
                    QFluentManager.google.download(name.lower())
                    return QIcon()

            return getattr(GoogleMaterialIconBase, name)
        except AttributeError as e:
            print(e)
            # 判断是否打包
            if not getattr(sys, 'frozen', False) and not '__compiled__' in globals():
                QFluentManager.google.download(name.lower())
            return QIcon()

    @classmethod
    def iconIfy(cls, name, theme=Theme.AUTO, reverse=False):
        try:
            icon_name = name.replace(":", "-").upper()
            IconifyIconBase.get(icon_name)

            # 判断是否打包
            if not getattr(sys, 'frozen', False) and not '__compiled__' in globals():
                theme = qconfig.theme if theme == Theme.AUTO else theme
                if os.path.exists(os.path.join(QFluentManager.iconify.getIconPath(),
                                               f"{icon_name.lower()}_{getIconColor(theme, reverse=reverse)}_{QFluentManager.iconify.size}.svg")):
                    return getattr(IconifyIconBase, icon_name)
                else:
                    QFluentManager.iconify.download(name.lower())
                    return QIcon()

            return getattr(IconifyIconBase, icon_name)
        except AttributeError as e:
            print(e)
            # 判断是否打包
            if not getattr(sys, 'frozen', False) and not '__compiled__' in globals():
                QFluentManager.iconify.download(name.lower())
            return QIcon()

    @classmethod
    def simpleIcons(cls, name, theme=Theme.AUTO, reverse=False):
        try:
            name = name.upper()
            SimpleIconsIconBase.get(name)

            # 判断是否打包
            if not getattr(sys, 'frozen', False) and not '__compiled__' in globals():
                theme = qconfig.theme if theme == Theme.AUTO else theme
                if os.path.exists(os.path.join(QFluentManager.simpleicons.getIconPath(),
                                               f"{name.lower()}_{getIconColor(theme, reverse=reverse)}_{QFluentManager.simpleicons.size}.svg")):
                    return getattr(SimpleIconsIconBase, name)
                else:
                    QFluentManager.simpleicons.download(name.lower())
                    return QIcon()

            return getattr(SimpleIconsIconBase, name)
        except AttributeError as e:
            print(e)
            # 判断是否打包
            if not getattr(sys, 'frozen', False) and not '__compiled__' in globals():
                QFluentManager.simpleicons.download(name.lower())
            return QIcon()

