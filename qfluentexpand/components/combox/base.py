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
    QWidget, QWidgetAction, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem
)

from qfluentwidgets.components.widgets.line_edit import LineEdit
from qfluentwidgets.common.animation import TranslateYAnimation
from qfluentwidgets.common.icon import FluentIconBase, isDarkTheme
from qfluentwidgets.common.icon import FluentIcon as FIF, Icon
from qfluentwidgets.common.font import setFont
from qfluentwidgets.common.style_sheet import FluentStyleSheet, themeColor
from qfluentwidgets.common.overload import singledispatchmethod



class Line(LineEdit):
    """ Line edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.hBoxLayout.setAlignment(Qt.AlignLeft)
        self.setReadOnly(True)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hBoxLayout.addItem(spacer)

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag.AlignLeft, *args, **kwargs):
        self.hBoxLayout.addWidget(widget, stretch=stretch, alignment=alignment, *args, **kwargs)

    def insertWidget(self, index: int, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag.AlignLeft, *args, **kwargs):
        self.hBoxLayout.insertWidget(index, widget, stretch=stretch, alignment=alignment, *args, **kwargs)

    def removeWidget(self, widget: QWidget):
        self.hBoxLayout.removeWidget(widget)


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

