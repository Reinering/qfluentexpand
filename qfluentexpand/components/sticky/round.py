#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import Union
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QMouseEvent, QCursor, QPainter, QPainterPath
from PySide6.QtWidgets import QWidget, QVBoxLayout

from qfluentwidgets import FluentIconBase

from qfluentexpand.components.widgets.pagesticky import PageSticky
from qfluentexpand.components.button.round import RoundPushButton, PrimaryRoundPushButton
from qfluentexpand.common.icon import APPICON



class StickyRoundButton(PageSticky):

    def __init__(self, text: str, parent: QWidget = None, icon: Union[QIcon, str, FluentIconBase] = None):
        super().__init__(parent)
        sticky_layout = QVBoxLayout(self)
        self.setLayout(sticky_layout)
        if icon is None:
            icon = APPICON.ARROW_DOWN
        self.button = PrimaryRoundPushButton(text, parent, icon)
        self.button.installEventFilter(self)
        self.button.clicked.connect(self.on_button_clicked)
        sticky_layout.addWidget(self.button)

    def on_button_clicked(self, callback=None):
        print('Button clicked')
        if callback:
            callback()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()
        path.addEllipse(self.rect())
        painter.fillPath(path, self.palette().window())

    def _resize_button(self):
        """调整按钮尺寸，使其充满整个 CircularStickyWidget"""
        self.button.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        """当控件大小改变时调整按钮大小"""
        super().resizeEvent(event)
        self._resize_button()