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
        self.setClearButtonEnabled(True)
        self.fileTypes = "*"
        self.state = False

        self.clearButton._icon = FIF.RIGHT_ARROW
        self.clearButton.clicked.disconnect()
        self.clearButton.clicked.connect(self._toggleSelect)

        self.textChanged.disconnect()
        self.textChanged.connect(self._onTextChanged)

    def setFileTypes(self, fileTypes):
        self.fileTypes = fileTypes

    def setText(self, arg__1: str) -> None:
        super().setText(arg__1)
        if arg__1:
            self.state = True
            self.clearButton._icon = FIF.CLOSE
        else:
            self.state = False
            self.clearButton._icon = FIF.RIGHT_ARROW

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.clearButton.setVisible(True)

    def _onTextChanged(self, text):
        if text:
            self.state = True
            self.clearButton._icon = FIF.CLOSE
        else:
            self.state = False
            self.clearButton._icon = FIF.RIGHT_ARROW

        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(text) and self.hasFocus())

    def _toggleSelect(self):
        if self.state:
            self.clear()
            self.state = False
            self.clearButton._icon = FIF.RIGHT_ARROW

            if self.isClearButtonEnabled():
                self.clearButton.setVisible(self.hasFocus())
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
            self.clearButton._icon = FIF.CLOSE


class FolderPathSelector(LineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Select a file folder")
        self.setReadOnly(True)
        self.setClearButtonEnabled(True)
        self.state = False

        self.clearButton._icon = FIF.RIGHT_ARROW
        self.clearButton.clicked.disconnect()
        self.clearButton.clicked.connect(self._toggleSelect)

        self.textChanged.disconnect()
        self.textChanged.connect(self._onTextChanged)

    def setText(self, arg__1: str) -> None:
        super().setText(arg__1)
        if arg__1:
            self.state = True
            self.clearButton._icon = FIF.CLOSE
        else:
            self.state = False
            self.clearButton._icon = FIF.RIGHT_ARROW

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.clearButton.setVisible(True)

    # 重载 mousePressEvent 确保按钮的点击优先级
    def mousePressEvent(self, event):
        # 如果点击在 clearButton 上，则优先处理按钮的点击
        if self.clearButton.underMouse():
            self.clearButton.click()  # 模拟按钮的点击事件
        else:
            super().mousePressEvent(event)

    def _onTextChanged(self, text):
        if text:
            self.state = True
            self.clearButton._icon = FIF.CLOSE
        else:
            self.state = False
            self.clearButton._icon = FIF.RIGHT_ARROW

        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(text) and self.hasFocus())

    def _toggleSelect(self):
        if self.state:
            self.clear()
            self.state = False
            self.clearButton._icon = FIF.RIGHT_ARROW

            if self.isClearButtonEnabled():
                self.clearButton.setVisible(self.hasFocus())
        else:
            try:
                folderPath = QFileDialog.getExistingDirectory(self, u"选择目录", "/",
                                                              QFileDialog.Option.ShowDirsOnly)
                if not folderPath:
                    return

                self.setText(folderPath)
            except Exception as e:
                print(e)

            self.state = True
            self.clearButton._icon = FIF.CLOSE
