#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


import sys
from typing import Union, List, Iterable

from PySide6.QtCore import Qt, Signal, QRectF, QPoint, QObject, QEvent, QTimer
from PySide6.QtGui import QPainter, QAction, QCursor, QIcon, QPainterPath
from PySide6.QtWidgets import (
    QWidget, QWidgetAction, QVBoxLayout, QHBoxLayout
)

from qfluentwidgets import MenuAnimationType, IndicatorMenuItemDelegate
from qfluentwidgets.common.icon import FluentIconBase, isDarkTheme
from qfluentwidgets.common.icon import FluentIcon as FIF, Icon
from qfluentwidgets.common.overload import singledispatchmethod

from qfluentexpand.components.menu.menu import RoundMenu



class Action(QWidgetAction):

    @singledispatchmethod
    def __init__(self, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.fluentIcon = None

    @__init__.register
    def _(self, text: str, parent: QObject = None, **kwargs):
        super().__init__(text, parent, **kwargs)
        self.fluentIcon = None

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QObject = None, **kwargs):
        super().__init__(icon, text, parent, **kwargs)
        self.fluentIcon = None

    @__init__.register
    def _(self, icon: FluentIconBase, text: str, parent: QObject = None, **kwargs):
        super().__init__(icon.icon(), text, parent, **kwargs)
        self.fluentIcon = icon

    def icon(self) -> QIcon:
        if self.fluentIcon:
            return Icon(self.fluentIcon)

        return super().icon()

    def setIcon(self, icon: Union[FluentIconBase, QIcon]):
        if isinstance(icon, FluentIconBase):
            self.fluentIcon = icon
            icon = icon.icon()

        super().setIcon(icon)


class ComboBoxMenu(RoundMenu):
    """ Combo box menu """

    def __init__(self, parent=None):
        super().__init__(title="", parent=parent)

        self.view.setViewportMargins(0, 2, 0, 6)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.view.setItemDelegate(IndicatorMenuItemDelegate())
        self.view.setObjectName('comboListWidget')

        self.setItemHeight(33)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        self.view.adjustSize(pos, aniType)
        self.adjustSize()
        return super().exec(pos, ani, aniType)