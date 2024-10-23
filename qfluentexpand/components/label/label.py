#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import Union
from typing import Optional
from PySide6.QtGui import Qt, QMovie, QPainter
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QLabel

from qfluentwidgets.common.style_sheet import FluentStyleSheet
from qfluentwidgets import FluentLabelBase, qconfig, getFont, theme
from qfluentwidgets.common.overload import singledispatchmethod

from qfluentexpand.common.gif import FluentGifBase, toQMovie



class GifLabel1(QLabel):
    def __init__(self, parent: Optional[QWidget] = None):
        super(GifLabel, self).__init__(parent=parent)
        self.movie_obj = None  # type: QMovie
        self.setScaledContents(True)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setGif(self, gif: Union[QMovie, FluentGifBase, str]):
        self.setScaledContents(True)
        self.setProperty('hasGif', gif is not None)
        self._gif = gif or QMovie()
        self.movie_obj = self.gif()
        self.setMovie(self.movie_obj)

    def setState(self, state):
        if state:
            self.movie_obj.start()
        else:
            self.movie_obj.stop()

    def gif(self):
        return toQMovie(self._gif)

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


class GifLabel(FluentLabelBase):
    """ Fluent GIF label"""

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._init()

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)

    def _init(self):
        FluentStyleSheet.LABEL.apply(self)
        self.setFont(self.getFont())
        self.setTextColor()
        qconfig.themeChangedFinished.connect(self.themeChangedFinished)

        self.customContextMenuRequested.connect(self._onContextMenuRequested)
        return self

    def setGif(self, gif: Union[QMovie, FluentGifBase, str]):
        self.setScaledContents(True)
        self.setProperty('hasGif', gif is not None)
        self._gif = gif or QMovie()
        self.movie_obj = self.gif()
        self.setMovie(self.movie_obj)

    def themeChangedFinished(self):
        self.movie_obj = self.gif()
        self.setMovie(self.movie_obj)

    def getFont(self):
        return getFont(14)

    def setState(self, state):
        if not self.movie_obj:
            return

        if state:
            self.movie_obj.start()
        else:
            self.movie_obj.stop()

    def gif(self):
        return toQMovie(self._gif)

    def setProperty(self, name: str, value) -> bool:
        if name != 'gif':
            return super().setProperty(name, value)

        self.setGif(value)
        return True

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