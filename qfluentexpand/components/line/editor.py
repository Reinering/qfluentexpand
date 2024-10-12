#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt

from qfluentwidgets.components.widgets.line_edit import LineEdit, LineEditButton
from qfluentwidgets.common.icon import FluentIcon as FIF




class LineEditor(LineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("input text here...")

        self.dropButton = LineEditButton(FIF.CLOSE, self)
        self.dropButton.setFixedSize(30, 25)
        self.setTextMargins(0, 0, 25, 0)  # right margin for dropButton
        self.dropButton.clicked.connect(self._toggleDrop)
        self.dropButton.hide()
        self.textChanged.connect(self._showDrop)
        self.hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignmentFlag.AlignRight)

    def setText(self, arg__1: str) -> None:
        super().setText(arg__1)

    def _showDrop(self, text):
        if text:
            self.dropButton.show()
        else:
            self.dropButton.hide()

    def _toggleDrop(self):
        self.clear()

