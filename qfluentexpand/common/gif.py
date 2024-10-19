#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from enum import Enum
from typing import Union
from PySide6.QtGui import QIconEngine, QIcon, QPixmap, QPainter
from PySide6.QtCore import QRect, QSize, QRectF
from PySide6.QtWidgets import QApplication, QLabel, QPushButton
from PySide6.QtGui import QMovie

from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig, getIconColor, PushButton, BodyLabel



class GifIconEngine(QIconEngine):
    def __init__(self, gif_path):
        super().__init__()
        self.movie = QMovie(gif_path)
        # self.movie.start()  # 开始播放 GIF

    def paint(self, painter, rect, mode, state):
        # 每次绘制时显示 GIF 的当前帧
        pixmap = self.movie.currentPixmap()
        painter.drawPixmap(rect, pixmap)

    def pixmap(self, size, mode, state):
        # 返回 GIF 的当前帧，适用于图标请求特定大小时
        return self.movie.currentPixmap().scaled(size)


class FluentGifBase:
    """ Fluent GIF base class """

    def path(self, theme=Theme.AUTO) -> str:
        """ Get the path of the GIF

        Parameters
        ----------
        theme: Theme
            the theme of the GIF
            * `Theme.Light`: GIF for light mode
            * `Theme.DARK`: GIF for dark mode
            * `Theme.AUTO`: GIF depends on `config.theme`
        """
        raise NotImplementedError

    def qmovie(self, theme=Theme.AUTO) -> QMovie:
        """ Return QMovie, which can be used to show GIF in widgets

        Parameters
        ----------
        theme: Theme
            the theme of the GIF
            * `Theme.Light`: GIF for light mode
            * `Theme.DARK`: GIF for dark mode
            * `Theme.AUTO`: GIF depends on `qconfig.theme`
        """
        path = self.path(theme)
        return QMovie(path)

    def render(self, painter, rect, theme=Theme.AUTO):
        """ Draw the GIF on the widget

        Parameters
        ----------
        painter: QPainter
            painter

        rect: QRect | QRectF
            the rect to render GIF

        theme: Theme
            the theme of the GIF
            * `Theme.Light`: GIF for light mode
            * `Theme.DARK`: GIF for dark mode
            * `Theme.AUTO`: GIF depends on `config.theme`
        """
        movie = self.movie(theme)
        current_frame = movie.currentPixmap()

        # Ensure the rect is a QRectF object for scaling
        if not isinstance(rect, QRectF):
            rect = QRectF(rect)

        # Draw the current frame of the GIF
        painter.drawPixmap(rect.toRect(), current_frame)

    def colored(self, lightGifPath: str, darkGifPath: str) -> "ColoredFluentGif":
        """ Create a colored fluent GIF based on theme

        Parameters
        ----------
        lightGifPath: str
            GIF path for light mode

        darkGifPath: str
            GIF path for dark mode
        """
        return ColoredFluentGif(self, lightGifPath, darkGifPath)


class ColoredFluentGif(FluentGifBase):
    """ Support different GIFs for light and dark themes """

    def __init__(self, gif: FluentGifBase, lightGifPath: str, darkGifPath: str):
        self.fluentGif = gif
        self.lightGifPath = lightGifPath
        self.darkGifPath = darkGifPath

    def path(self, theme=Theme.AUTO) -> str:
        """ Return the appropriate GIF path based on the theme """
        return self.fluentGif.path(theme)

    def render(self, painter, rect, theme=Theme.AUTO, indexes=None, **attributes):
        print("ColoredFluentGift render method")


def toQMovie(gif: Union[QMovie, FluentGifBase, str]) -> QMovie:
    """ convet `icon` to `QIcon` """
    if isinstance(gif, str):
        return QMovie(gif)

    if isinstance(gif, FluentGifBase):
        return gif.qmovie()

    return gif


class APPGIF(FluentGifBase, Enum):

    LOADING = "loading"
    LOADINGV2 = "loadingv2"
    LOADINGV3 = "loadingv3"
    LOADINGV4 = "loadingv4"
    LOADINGV5 = "loadingv5"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/qfluentexpand/gifs/{theme.value.lower()}/{self.value.lower()}.gif"