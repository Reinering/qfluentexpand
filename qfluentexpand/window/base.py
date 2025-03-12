#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""



import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMainWindow

from qframelesswindow.titlebar import TitleBar, TitleBarButton, SvgTitleBarButton, StandardTitleBar, TitleBarBase

if sys.platform == "win32":
    from qframelesswindow.windows import AcrylicWindow
    from qframelesswindow.windows import WindowsFramelessWindow as FramelessWindow
    from qframelesswindow.windows import WindowsFramelessMainWindow as FramelessMainWindow
    from qframelesswindow.windows import WindowsFramelessDialog as FramelessDialog
    from qframelesswindow.windows import WindowsWindowEffect as WindowEffect
    from qframelesswindow.windows import WindowsFramelessWindowBase as FramelessWindowBase
elif sys.platform == "darwin":
    from qframelesswindow.mac import AcrylicWindow
    from qframelesswindow.mac import MacFramelessWindow as FramelessWindow
    from qframelesswindow.mac import MacFramelessMainWindow as FramelessMainWindow
    from qframelesswindow.mac import MacFramelessDialog as FramelessDialog
    from qframelesswindow.mac import MacWindowEffect as WindowEffect
    from qframelesswindow.mac import MacFramelessWindowBase as FramelessWindowBase
else:
    from qframelesswindow.linux import LinuxFramelessWindow as FramelessWindow
    from qframelesswindow.linux import LinuxFramelessMainWindow as FramelessMainWindow
    from qframelesswindow.linux import LinuxFramelessDialog as FramelessDialog
    from qframelesswindow.linux import LinuxWindowEffect as WindowEffect
    from qframelesswindow.linux import LinuxFramelessWindowBase as FramelessWindowBase

    AcrylicWindow = FramelessWindow