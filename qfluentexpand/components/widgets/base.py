#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import Union
from PySide6.QtCore import Property, Qt, QSize, QRectF, Signal, QPointF, QPoint, QRect
from PySide6.QtGui import QColor, QPainter, QPainterPath, QIcon
from PySide6.QtWidgets import QWidget, QApplication

from qfluentwidgets.components.settings.setting_card import SettingIconWidget
from qfluentwidgets.common.icon import FluentIconBase, drawIcon, isDarkTheme, Theme, toQIcon, Icon
from qfluentwidgets.common.style_sheet import FluentStyleSheet
from qfluentwidgets.common.font import setFont, getFont
from qfluentwidgets.common.overload import singledispatchmethod
from qfluentwidgets.common.font import setFont, getFont


class QFWidget1(QWidget):

    singal_click = Signal()

    @singledispatchmethod
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化默认属性值
        self._fill_color = QColor("#transparent")
        self._border_color = QColor("#transparent")
        self._border_width = 1

        self._icon = None
        self._icon_size = QSize(16, 16)  # 默认图标大小
        self.setIcon(None)
        setFont(self)

        self._text = ""

        self.isPressed = False
        self.isHover = False
        self.m_last_pos = QPointF()
        self.isMoving = False
        self.enable_move = False

        self._postInit()

    @__init__.register
    def _(self, text: str, parent: QWidget = None, icon: Union[QIcon, str, "FluentIconBase"] = None):
        self.__init__(parent=parent)
        self.setText(text)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    @__init__.register
    def _(self, icon: "FluentIconBase", text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    def _postInit(self):
        pass

    # 填充颜色属性 (qproperty-fillColor)
    @Property(QColor)
    def fillColor(self):
        return self._fill_color

    @fillColor.setter
    def fillColor(self, color):
        self._fill_color = color
        self.update()

    # 边框颜色属性 (qproperty-borderColor)
    @Property(QColor)
    def borderColor(self):
        return self._border_color

    @borderColor.setter
    def borderColor(self, color):
        self._border_color = color
        self.update()

    # 边框粗细属性 (qproperty-borderWidth)
    @Property(int)
    def borderWidth(self):
        return self._border_width

    @borderWidth.setter
    def borderWidth(self, width):
        self._border_width = width
        self.update()

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)


        if e.button() == Qt.MouseButton.LeftButton:
            self.m_last_pos = e.globalPosition()
            self.isMoving = False
            e.accept()

        self.update()

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

        if e.button() == Qt.MouseButton.LeftButton and self.enable_move:
            if not self.isMoving:
                self.singal_click.emit()
            self.isMoving = False
            e.accept()

        self.update()

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton  and self.enable_move:
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

    def _drawIcon(self, icon, painter, rect, state=QIcon.State.Off):
        drawIcon(icon, painter, rect, state)

    def paintEvent(self, event):
        """
        基类接管 paintEvent，负责通用的绘图准备工作。
        具体的‘形状路径’交给子类去实现。
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # 开启抗锯齿

        # 获取子类提供的具体形状路径 (QPainterPath)
        path = self.getShapePath()
        if path.isEmpty():
            return

        # 设置画刷（填充色）
        painter.setBrush(self._fill_color)

        # 设置画笔（边框）
        if self._border_width > 0 and self._border_color.alpha() > 0:
            painter.setPen(Qt.PenStyle.SolidLine)
            painter.setPen(self._border_color)
            # 动态调整画笔粗细
            pen = painter.pen()
            pen.setWidth(self._border_width)
            painter.setPen(pen)
        else:
            painter.setPen(Qt.PenStyle.NoPen)

        # 核心：绘制子类定义的形状
        painter.drawPath(path)

        diameter = min(self.width(), self.height())
        rect = QRectF((self.width() - diameter) / 2, (self.height() - diameter) / 2, diameter, diameter)

        # 绘制文本
        if self.text():
            painter.setPen(Qt.GlobalColor.black if self.isEnabled() else Qt.GlobalColor.gray)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())

        # 新增：在形状中心绘制 Icon
        if not self._icon.isNull():
            # # 计算居中的矩形位置
            # rect = self.contentsRect()
            # icon_width = self._icon_size.width()
            # icon_height = self._icon_size.height()
            #
            # # 让图标在组件的 contentsRect 中心居中
            # icon_rect = [
            #     int(rect.center().x() - icon_width / 2),
            #     int(rect.center().y() - icon_height / 2),
            #     icon_width,
            #     icon_height
            # ]
            #
            # # 使用 QIcon 的 paint 方法绘制，它会自动处理 :hover 或 :disabled 状态下的图标变暗/变亮效果
            # self._icon.paint(painter, *icon_rect, Qt.AlignmentFlag.AlignCenter)

            # 居中计算图标的位置
            w, h = self.iconSize().width(), self.iconSize().height()
            x = (self.width() - w) / 2
            y = (self.height() - h) / 2

            self._drawIcon(self._icon, painter, QRectF(x, y, w, h))

    def getShapePath(self) -> QPainterPath:
        """
        虚方法/留空方法：专门等待子类去重写。
        子类只需要返回自己想画的形状路径即可。
        """
        return QPainterPath()


class QFWidget(QWidget):
    """ QFWidget
    """

    signal_click = Signal()

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._lightTextColor = QColor(0, 0, 0)
        self._darkTextColor = QColor(255, 255, 255)
        self.lightIndicatorColor = QColor()
        self.darkIndicatorColor = QColor()
        self.indicatorPos = QPoint(11, 12)
        self.m_last_pos = QPointF()

        self.isPressed = False
        self.isHover = False
        self.isMoving = False
        self.isEnabledMove = False

        self._text = ''

        self.setIconSize(QSize(16, 16))
        self.setIcon(None)

        self.setFixedSize(64, 64)

        self._alpha = 1.0
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

    def setAlpha(self, alpha: float):
        self._alpha = alpha
        self.update()

    def alpha(self):
        return self._alpha

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
        painter.drawText(QRect(0, 0, self.width() - 1, self.height() - 1), Qt.AlignmentFlag.AlignVCenter, self.text())

    def _drawIndicator(self, painter: QPainter):
        if self.isEnabled():
            if self.isPressed:
                filledColor = Qt.GlobalColor.black if isDarkTheme() else Qt.GlobalColor.white
            elif self.isHover:
                filledColor = QColor(0, 0, 0, 11) if isDarkTheme() else QColor(0, 0, 0, 15)
            else:
                filledColor = QColor(0, 0, 0, int(self.alpha()*255)) if isDarkTheme() else QColor(0, 0, 0, int(self.alpha()*255))
        else:
            filledColor = QColor(0, 0, 0, 20) if isDarkTheme() else QColor(0, 0, 0, 25)

        self._drawCircle(painter, self.indicatorPos, filledColor)

    def _drawCircle(self, painter: QPainter, center: QPoint, filledColor):
        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)
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