#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog

from qfluentwidgets.components.widgets.line_edit import LineEdit, LineEditButton
from qfluentwidgets.common.icon import FluentIcon as FIF


class FilePathSelector(LineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Select a file path")
        self.setReadOnly(True)
        self.fileTypes = "*"
        self.state = False

        self.dropButton = LineEditButton(FIF.RIGHT_ARROW, self)
        self.dropButton.setFixedSize(30, 25)
        self.setTextMargins(0, 0, 25, 0)    # right margin for dropButton
        self.dropButton.clicked.connect(self._toggleSelect)
        self.hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignmentFlag.AlignRight)

    def setFileTypes(self, fileTypes):
        self.fileTypes = fileTypes

    def setText(self, arg__1: str) -> None:
        super().setText(arg__1)
        if arg__1:
            self.state = True
            self.dropButton._icon = FIF.CLOSE
        else:
            self.state = False
            self.dropButton._icon = FIF.RIGHT_ARROW

    def _toggleSelect(self):
        if self.state:
            self.clear()
            self.state = False
            self.dropButton._icon = FIF.RIGHT_ARROW
        else:
            try:
                filePath = QFileDialog.getOpenFileName(self, u"选择文件", "/",
                                                       self.fileTypes)
                if not filePath[0]:
                    return

                self.setText(filePath[0])
            except Exception as e:
                print(e)
            self.state = True
            self.dropButton._icon = FIF.CLOSE



class FolderPathSelector(LineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Select a file folder")
        self.setReadOnly(True)

        self.dropButton = LineEditButton(FIF.RIGHT_ARROW, self)
        self.dropButton.setFixedSize(30, 25)
        self.setTextMargins(0, 0, 25, 0)    # right margin for dropButton
        self.dropButton.clicked.connect(self._toggleSelect)
        self.hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignmentFlag.AlignRight)

    def _toggleSelect(self):
        try:
            folderPath = QFileDialog.getExistingDirectory(self, u"选择目录", "/",
                                                          QFileDialog.Option.ShowDirsOnly)
            if not folderPath:
                return

            self.setText(folderPath)
        except Exception as e:
            print(e)

