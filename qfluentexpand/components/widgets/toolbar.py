#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import List, Union
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QToolBar,  QStyleFactory, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QAction, QIcon

from qfluentwidgets import setFont, FluentIcon, isDarkTheme, FluentIconBase, qconfig, Icon, Action as QA

from ...common.stylesheets import STYLESHEET


class Action(QA):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qconfig.themeChangedFinished.connect(self.themeChangedFinished)

    def themeChangedFinished(self):
        if self.fluentIcon:
            self.setIcon(self.fluentIcon)


class ToolBar(QToolBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initWidget()

        STYLESHEET.TOOLBAR.apply(self)

    def initWidget(self):
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.NoDropShadowWindowHint)
        setFont(self, 12)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.setStyle(QStyleFactory.create("fusion"))





