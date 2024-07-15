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

        items = ['shoko 🥰', '西宫硝子', 'aiko', '柳井爱子']
        self.comboBox = MSEComboBox(self)
        self.comboBox.setMinimumWidth(200)
        self.comboBox.setPlaceholderText("选择一个脑婆")
        self.comboBox.addItems(items)
        # self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignCenter)


        # self.comboBox.setReadOnly(False)
        # self.comboBox.setCurrentIndex(0)
        self.comboBox.currentTextChanged.connect(print)
        self.comboBox.move(200, 200)

        # NOTE: Completer is only applicable to EditableComboBox
        # self.completer = QCompleter(items, self)
        # self.comboBox.setCompleter(self.completer)

        self.resize(500, 500)
        self.setStyleSheet('Demo{background:white}')

        # setTheme(Theme.DARK)
        # setThemeColor('#0078d4')


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Ceil)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()