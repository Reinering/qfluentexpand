#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import Optional
from PySide6.QtGui import Qt, QMovie, QPainter
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QLabel



class GifLabel(QLabel):
    def __init__(self, parent: Optional[QWidget] = None):
        super(GifLabel, self).__init__(parent=parent)
        self.movie_obj = None  # type: QMovie
        self.setScaledContents(True)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setGif(self, gif_path):
        self.movie_obj = QMovie(gif_path)
        self.setMovie(self.movie_obj)

    def setState(self, state):
        if state:
            self.movie_obj.start()
        else:
            self.movie_obj.stop()

    def paintEvent(self, event):
        # 重写动画的绘制事件，使用自带的会导致动画模糊有锯齿
        if self.movie_obj and self.movie_obj.isValid():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            curr_pix = self.movie_obj.currentPixmap()
            if self.hasScaledContents():
                pix = curr_pix.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
                painter.drawPixmap(QPoint(0, 0), pix)
            else:
                painter.drawPixmap(QPoint(0, 0), curr_pix)
        else:
            super().paintEvent(event)