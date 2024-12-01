#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import Union
from PySide6.QtCore import Signal, QUrl, Qt, QRectF, QSize, QPoint, Property
from PySide6.QtGui import QDesktopServices, QIcon, QPainter, QColor, QPainterPath
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QRadioButton, QToolButton, QApplication, QWidget, QSizePolicy

from qfluentwidgets import setFont, Theme, isDarkTheme
from qfluentwidgets.common.icon import FluentIconBase, toQIcon, drawIcon
from qfluentwidgets.common.overload import singledispatchmethod

from qfluentexpand.common.stylesheets import STYLESHEET


class RoundPushButton(QPushButton):
    """ Push RoundPushButton

    Constructors
    ------------
    * RoundPushButton(`parent`: QWidget = None)
    * RoundPushButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * RoundPushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        STYLESHEET.BUTTON.apply(self)
        self.isPressed = False
        self.isHover = False
        self.setIconSize(QSize(16, 16))
        self.setIcon(None)
        setFont(self)
        self._postInit()
        self.setBaseSize(40, 40)

    @__init__.register
    def _(self, text: str, parent: QWidget = None, icon: Union[QIcon, str, FluentIconBase] = None):
        self.__init__(parent=parent)
        self.setText(text)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    @__init__.register
    def _(self, icon: FluentIconBase, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    def _postInit(self):
        pass

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase]):
        self.setProperty('hasIcon', icon is not None)
        self.setStyle(QApplication.style())
        self._icon = icon or QIcon()
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setProperty(self, name: str, value) -> bool:
        if name != 'icon':
            return super().setProperty(name, value)

        self.setIcon(value)
        return True

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def enterEvent(self, e):
        self.isHover = True
        self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self.update()

    def _drawIcon(self, icon, painter, rect, state=QIcon.State.Off):
        """ draw icon """
        drawIcon(icon, painter, rect, state)

    def paintEvent(self, e):

        if self.icon().isNull():
            return
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)

        if self.width() != self.height():
            self.setFixedSize(self.height(), self.height())
        # Draw circular background
        path = QPainterPath()
        radius = min(self.width(), self.height()) / 2
        path.addEllipse(self.rect())
        painter.setClipPath(path)

        if not self.isEnabled():
            painter.setOpacity(0.3628)
        elif self.isPressed:
            painter.setOpacity(0.786)
        elif self.isHover:
            painter.setOpacity(0.686)
        else:
            painter.setOpacity(1.0)

        painter.fillPath(path, self.palette().button())

        # Draw text if present
        if self.text():
            painter.setPen(self.palette().buttonText().color())
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        # Draw icon if present
        elif not self.icon().isNull():
            w, h = self.iconSize().width(), self.iconSize().height()
            # x = (self.width() - w) / 2
            # y = (self.height() - h) / 2

            y = (self.height() - h) / 2
            mw = self.minimumSizeHint().width()
            if mw > 0:
                x = 12 + (self.width() - mw) // 2
            else:
                x = 12

            if self.isRightToLeft():
                x = self.width() - w - x

            self._drawIcon(self._icon, painter, QRectF(x, y, w, h))
        # super().paintEvent(e)
        painter.end()


class PrimaryRoundPushButton(RoundPushButton):
    """ Primary color round push button

    Constructors
    ------------
    * PrimaryRoundPushButton(`parent`: QWidget = None)
    * PrimaryRoundPushButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * PrimaryRoundPushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    def _drawIcon(self, icon, painter, rect, state=QIcon.State.Off):
        if isinstance(icon, FluentIconBase) and self.isEnabled():
            # reverse icon color
            theme = Theme.DARK if not isDarkTheme() else Theme.LIGHT
            icon = icon.icon(theme)
        elif not self.isEnabled():
            painter.setOpacity(0.786 if isDarkTheme() else 0.9)
            if isinstance(icon, FluentIconBase):
                icon = icon.icon(Theme.DARK)

        RoundPushButton._drawIcon(self, icon, painter, rect, state)