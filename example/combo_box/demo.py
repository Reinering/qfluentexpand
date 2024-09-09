#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QCompleter, QVBoxLayout

from qfluentwidgets import ComboBox, setTheme, Theme, setThemeColor, EditableComboBox
from qfluentexpand.components.combox.combo_box import MSEComboBox, MSECComboBox

class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.vboxlayout = QVBoxLayout(self)

        items = ['shoko 🥰', '西宫硝子', 'aiko', '柳井爱子']
        self.comboBox1_1 = MSEComboBox(self)
        self.comboBox1_1.setMinimumWidth(300)
        self.comboBox1_1.setPlaceholderText("选择一个脑婆")
        self.comboBox1_1.addItems(items)
        self.comboBox1_1.currentTextChanged.connect(print)
        self.vboxlayout.addWidget(self.comboBox1_1, 0, Qt.AlignCenter)

        # NOTE: Completer is only applicable to EditableComboBox
        # self.completer = QCompleter(items, self)
        # self.comboBox.setCompleter(self.completer)

        self.comboBox1_2 = MSEComboBox(self)
        self.comboBox1_2.setMinimumWidth(300)
        self.comboBox1_2.setPlaceholderText("选择一个脑婆")
        self.comboBox1_2.addItems(items)
        self.comboBox1_2.setReadOnly(False)
        self.comboBox1_2.currentTextChanged.connect(print)
        self.vboxlayout.addWidget(self.comboBox1_2, 0, Qt.AlignCenter)

        items = {'shoko': ["Item 1", "Item 2", "Item 3", "Item 4"],
                                   '西宫硝子': ["Item 1", "Item 2", "Item 3", "Item 4"],
                                   '宝多六花': ["Item 1", "Item 2", "Item 3", "Item 4"],
                                   '小鸟游六花': ["Item 1", "Item 2", "Item 3", "Item 4"]}
        self.comboBox2_1 = MSECComboBox(self)
        self.comboBox2_1.setMinimumWidth(300)
        self.comboBox2_1.setPlaceholderText("选择一个脑婆")
        self.comboBox2_1.addItems(items)
        self.comboBox2_1.setReadOnly(False)
        self.comboBox2_1.currentTextChanged.connect(print)
        self.vboxlayout.addWidget(self.comboBox2_1, 0, Qt.AlignCenter)

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