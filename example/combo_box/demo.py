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
        self.comboBox1_1 = MSEComboBox(self)
        self.comboBox1_1.setMinimumWidth(200)
        self.comboBox1_1.setPlaceholderText("选择一个脑婆")
        self.comboBox1_1.addItems(items)
        # self.hBoxLayout.addWidget(self.comboBox1_1, 0, Qt.AlignCenter)


        # self.comboBox.setReadOnly(False)
        # self.comboBox.setCurrentIndex(0)
        self.comboBox1_1.currentTextChanged.connect(print)
        self.comboBox1_1.move(200, 200)

        # NOTE: Completer is only applicable to EditableComboBox
        # self.completer = QCompleter(items, self)
        # self.comboBox.setCompleter(self.completer)

        self.comboBox1_2 = MSEComboBox(self)
        self.comboBox1_2.setMinimumWidth(200)
        self.comboBox1_2.setPlaceholderText("选择一个脑婆")
        self.comboBox1_2.addItems(items)
        self.comboBox1_2.setReadOnly(False)
        self.comboBox1_2.currentTextChanged.connect(print)
        self.comboBox1_2.move(200, 250)

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