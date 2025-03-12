#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import QPoint, QEvent, Qt
from PySide6.QtGui import QCursor, QMouseEvent, QKeySequence
from PySide6.QtWidgets import QApplication, QMdiSubWindow, QMdiArea
from ctypes.wintypes import MSG
import win32con
import sys

from qframelesswindow import TitleBarBase
from qframelesswindow.linux import LinuxFramelessWindowBase
from qframelesswindow.windows import WindowsFramelessWindowBase
from qframelesswindow.titlebar.title_bar_buttons import TitleBarButtonState

from qfluentexpand.window.fluent_window import FluentTitleBar

from .base import FramelessWindowBase




class SubWindow(FramelessWindowBase, QMdiSubWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initFrameless()

        self.setContentsMargins(1, 30, 1, 1)
        self.setTitleBar(FluentTitleBar(self))

        self.titleBar.raise_()

    def setTitleBar(self, titleBar):
        super().setTitleBar(titleBar)

        # hide title bar buttons on macOS
        if sys.platform == "darwin" and self.isSystemButtonVisible() and isinstance(titleBar, TitleBarBase):
            titleBar.minBtn.hide()
            titleBar.maxBtn.hide()
            titleBar.closeBtn.hide()

    def resizeEvent(self, e):
        self.titleBar.move(5, 0)
        self.titleBar.resize(self.width()-5, self.titleBar.height())

    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        # msg = MSG.from_address(message.__int__())
        # if not msg.hWnd:
        #     return super().nativeEvent(eventType, message)
        #
        # if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
        #     if self._isHoverMaxBtn():
        #         self.titleBar.maxBtn.setState(TitleBarButtonState.HOVER)
        #         return True, win32con.HTMAXBUTTON
        #
        # elif msg.message in [0x2A2, win32con.WM_MOUSELEAVE]:
        #     self.titleBar.maxBtn.setState(TitleBarButtonState.NORMAL)
        # elif msg.message in [win32con.WM_NCLBUTTONDOWN, win32con.WM_NCLBUTTONDBLCLK] and self._isHoverMaxBtn():
        #     e = QMouseEvent(QEvent.Type.MouseButtonPress, QPoint(), Qt.MouseButton.LeftButton, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
        #     QApplication.sendEvent(self.titleBar.maxBtn, e)
        #     return True, 0
        # elif msg.message in [win32con.WM_NCLBUTTONUP, win32con.WM_NCRBUTTONUP] and self._isHoverMaxBtn():
        #     e = QMouseEvent(QEvent.Type.MouseButtonRelease, QPoint(), Qt.MouseButton.LeftButton, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
        #     QApplication.sendEvent(self.titleBar.maxBtn, e)
        #
        # return super().nativeEvent(eventType, message)
        pass

    def _isHoverMaxBtn(self):
        pos = QCursor.pos() - self.geometry().topLeft() - self.titleBar.pos()
        return self.titleBar.childAt(pos) is self.titleBar.maxBtn
