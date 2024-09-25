#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

from qfluentexpand.components.label.label import GifLabel


class Spinner(GifLabel):
    """
    Spinner widget
    """

    def __init__(self, parent=None):
        super(Spinner, self).__init__(parent)
        self.setFixedSize(30, 30)


