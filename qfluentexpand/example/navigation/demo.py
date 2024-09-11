#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QCompleter
from qfluentwidgets import ComboBox, setTheme, Theme, setThemeColor, EditableComboBox
from qfluentexpand.components.combox.combo_box import MSEComboBox

class Demo(QWidget):

    def __init__(self):
        super().__init__()




if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Ceil)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()