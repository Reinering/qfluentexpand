#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
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
        self.hBoxLayout.insertItem(0, spacer)

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag.AlignLeft, *args, **kwargs):
        self.hBoxLayout.addWidget(widget, stretch=stretch, alignment=alignment, *args, **kwargs)

    def insertWidget(self, index: int, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag.AlignLeft, *args, **kwargs):
        self.hBoxLayout.insertWidget(index, widget, stretch=stretch, alignment=alignment, *args, **kwargs)

    def removeWidget(self, widget: QWidget):
        self.hBoxLayout.removeWidget(widget)


class ShortcutRecorderLineEdit(LineEdit):
    """Shortcut Recorder Line Edit"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("点击此处并按下快捷键...")
        self.setReadOnly(True)  # 禁止用户直接输入文本
        self.current_sequence = None

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()

        # 1. 忽略单独按下修饰键的情况
        if key in [Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta]:
            return

        # 2. 如果按下 Backspace 或 Delete，清空已录制的快捷键
        if key in [Qt.Key.Key_Backspace, Qt.Key.Key_Delete]:
            self.clear()
            self.current_sequence = None
            return

        # 3. 处理组合键（直接使用位运算符 | 组合枚举和键值）
        extracted_key = modifiers.value | key

        # 4. 转换为 QKeySequence 并显示
        self.current_sequence = QKeySequence(extracted_key)
        self.setText(self.current_sequence.toString())

        self.clearFocus()