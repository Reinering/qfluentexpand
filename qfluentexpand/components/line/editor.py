#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QSizePolicy, QSpacerItem
)

from qfluentwidgets.components.widgets.line_edit import LineEdit, LineEditButton
from qfluentwidgets.common.icon import FluentIcon as FIF



class Line(LineEdit):
    """ Line edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setReadOnly(True)
        self.setClearButtonEnabled(True)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hBoxLayout.addItem(spacer)

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag.AlignLeft, *args, **kwargs):
        self.hBoxLayout.addWidget(widget, stretch=stretch, alignment=alignment, *args, **kwargs)

    def insertWidget(self, index: int, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag.AlignLeft, *args, **kwargs):
        self.hBoxLayout.insertWidget(index, widget, stretch=stretch, alignment=alignment, *args, **kwargs)

    def removeWidget(self, widget: QWidget):
        self.hBoxLayout.removeWidget(widget)


