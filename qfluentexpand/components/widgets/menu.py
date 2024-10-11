#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import Union
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QIcon

from qfluentwidgets import RoundMenu, Action
from qfluentwidgets.common.icon import FluentIcon, FluentIconBase

import os


class ListSubMenu(RoundMenu):
    fileSelected = Signal(str)  # 当选择一个文件时发出信号

    def __init__(self, icon: Union[FluentIconBase, QIcon], text, recent_files=[], max_count=10, parent=None):
        super().__init__(text, parent)
        self.setIcon(icon)
        self.max_count = max_count
        self.recent_files = recent_files
        self.updateMenu()

    def addFile(self, filepath):
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        if len(self.recent_files) > self.max_count:
            self.recent_files.pop()
        self.updateMenu()

    def updateMenu(self):
        self.clear()
        for filepath in self.recent_files:
            if os.path.basename(filepath):
                action = Action(FluentIcon.BASKETBALL, os.path.basename(filepath))
            else:
                action = Action(FluentIcon.BASKETBALL, filepath)
            action.setStatusTip(filepath)
            action.triggered.connect(lambda checked, path=filepath: self.fileSelected.emit(path))
            self.addAction(action)

        if not self.recent_files:
            self.addAction(Action(FluentIcon.BASKETBALL, "None"))

    def getRecentFiles(self):
        return self.recent_files

    def setRecentFiles(self, files):
        self.recent_files = files[:self.max_count]
        self.updateMenu()