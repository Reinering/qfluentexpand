#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import Union

from PySide6.QtCore import Qt, QPointF, Signal, QSize, QRectF, QPoint, QRect, Property
from PySide6.QtGui import QPainter, QColor, QFont, QIcon, QPen, QPainterPath
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QPushButton
import sys

from qfluentwidgets.components.settings.setting_card import SettingIconWidget
from qfluentwidgets.common.icon import FluentIconBase, drawIcon, isDarkTheme, Theme, toQIcon, Icon
from qfluentwidgets.common.style_sheet import FluentStyleSheet
from qfluentwidgets.common.font import setFont, getFont
from qfluentwidgets.common.overload import singledispatchmethod

from ...components.widgets.base import QFWidget

from ...common.stylesheets import STYLESHEET



class FloatingBall(QFWidget):
    """ FloatingBall
    """

    signal_click = Signal()

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # STYLESHEET.FLOATING_BALL.apply(self)

        self._alpha = 0.0605

        self.setFixedSize(64, 64)
        self._radius = 12

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |  # 确保永远在最前，不会因弹窗消失
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._postInit()

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)

    def _postInit(self):
        pass

    def setText(self, text: str):
        self._text = text
        self.update()

    def text(self):
        return self._text

    def setIconSize(self, size: QSize):
        self._icon_size = size
        self.update()

    def iconSize(self):
        return self._icon_size

    def setIcon(self, icon: Union[QIcon, str, "FluentIconBase"]):
        if icon is None or (isinstance(icon, QIcon) and icon.isNull()):
            self.setProperty('hasIcon', False)
        else:
            self.setProperty('hasIcon', True)

        self.setStyle(QApplication.style())
        self._icon = icon or QIcon()
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

        if e.button() == Qt.MouseButton.LeftButton and self.isEnabledMove:
            self.m_last_pos = e.globalPosition()
            self.isMoving = False
            e.accept()

        self.update()

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

        if e.button() == Qt.MouseButton.LeftButton and self.isEnabledMove:
            if not self.isMoving:
                self.signal_click.emit()
            self.isMoving = False
            e.accept()

        self.update()

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton  and self.isEnabledMove:
            current_pos = e.globalPosition()
            delta = current_pos - self.m_last_pos

            # 如果移动距离太小（比如颤抖了1像素），不判定为拖拽
            if delta.manhattanLength() > 1:
                self.isMoving = True

            self.move(self.pos() + delta.toPoint())
            self.m_last_pos = current_pos
            e.accept()

            self.update()

    def enterEvent(self, e):
        self.isHover = True
        self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self._drawIndicator(painter)
        if self.text():
            self._drawText(painter)

        if not self.icon().isNull():
            self._drawIcon(self.icon(), painter)

    def _drawText(self, painter: QPainter):
        if not self.isEnabled():
            painter.setOpacity(0.36)

        painter.setFont(self.font())
        painter.setPen(self.textColor())
        painter.drawText(QRect(0, 0, self.width() - 1, self.height() - 1), Qt.AlignmentFlag.AlignCenter, self.text())

    def _drawIndicator(self, painter: QPainter):
        if self.isEnabled():
            if self.isPressed:
                filledColor = QColor(0, 0, 0, int(0.786*255)) if isDarkTheme() else QColor(249, 249, 249, int(0.3*255))
            elif self.isHover:
                filledColor = QColor(0, 0, 0, int(0.0837*255)) if isDarkTheme() else QColor(249, 249, 249, int(0.5*255))
            else:
                filledColor = QColor(0, 0, 0, int(self.alpha()*255)) if isDarkTheme() else QColor(249, 249, 249, int(self.alpha()*255))
        else:
            filledColor = QColor(0, 0, 0, 0.3628) if isDarkTheme() else QColor(249, 249, 249, 0.3)

        self._drawCircle(painter, self.indicatorPos, filledColor)

    def _drawCircle(self, painter: QPainter, center: QPoint, filledColor):
        path = QPainterPath()
        painter.setPen(Qt.PenStyle.NoPen)       # 取消边框
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # 开启抗锯齿

        diameter = min(self.width(), self.height())

        rect = QRectF((self.width() - diameter) / 2, (self.height() - diameter) / 2, diameter, diameter)
        painter.setBrush(filledColor)
        painter.drawEllipse(rect)

    def _drawIcon(self, icon, painter, state=QIcon.State.Off):
        # 设置图标透明度
        if not self.isEnabled():
            painter.setOpacity(0.3628)
        elif self.isHover:
            painter.setOpacity(0.8)
        elif self.isPressed:
            painter.setOpacity(0.786)
        else:
            painter.setOpacity(1.0)

        # 居中计算图标的位置
        w, h = self.iconSize().width(), self.iconSize().height()
        x = (self.width() - w) / 2
        y = (self.height() - h) / 2

        drawIcon(icon, painter, QRectF(x, y, w, h), state)

    def textColor(self):
        return self.darkTextColor if isDarkTheme() else self.lightTextColor

    def getLightTextColor(self) -> QColor:
        return self._lightTextColor

    def getDarkTextColor(self) -> QColor:
        return self._darkTextColor

    def setLightTextColor(self, color: QColor):
        self._lightTextColor = QColor(color)
        self.update()

    def setDarkTextColor(self, color: QColor):
        self._darkTextColor = QColor(color)
        self.update()

    def setIndicatorColor(self, light, dark):
        self.lightIndicatorColor = QColor(light)
        self.darkIndicatorColor = QColor(dark)
        self.update()

    def setTextColor(self, light, dark):
        self.setLightTextColor(light)
        self.setDarkTextColor(dark)

    lightTextColor = Property(QColor, getLightTextColor, setLightTextColor)
    darkTextColor = Property(QColor, getDarkTextColor, setDarkTextColor)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ball = FloatingBall()
    ball.show()
    sys.exit(app.exec())