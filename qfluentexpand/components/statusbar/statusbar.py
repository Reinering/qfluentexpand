#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout


class StatusBarBase(QWidget):

    def __init__(self, parent=None):
        super(StatusBarBase, self).__init__(parent)
        self.setFixedHeight(30)
        self.hBoxLayout = QHBoxLayout()
        self.setLayout(self.hBoxLayout)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setObjectName("HBoxLayout")
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)

    def removeWidget(self, widget):
        self.hBoxLayout.removeWidget(widget)

    def insertWidget(self, index, widget):
        self.hBoxLayout.insertWidget(index, widget)

    def addSpacing(self, spacing):
        self.hBoxLayout.addSpacing(spacing)

    def setSpacing(self, spacing):
        self.hBoxLayout.setSpacing(spacing)

    def addLayout(self, layout):
        self.hBoxLayout.addLayout(layout)

    def layout(self):
        return self.hBoxLayout.layout()

    def setContentsMargins(self, x, y, a, b):
        self.hBoxLayout.setContentsMargins(x, y, a, b)

    def setAlignment(self, alignment):
        self.hBoxLayout.setAlignment(alignment)

