#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt, QPointF, Signal, QSize, QRectF
from PySide6.QtGui import QPainter, QColor, QFont, QIcon, QPen, QPainterPath
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QPushButton
import sys

from qfluentwidgets.components.widgets.base import QFWidget



class TriangleWidget(QFWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |  # 确保永远在最前，不会因弹窗消失
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def getShapePath(self) -> QPainterPath:
        # 使用 contentsRect()，自动支持 QSS 的 padding 留白
        rect = self.contentsRect()
        path = QPainterPath()

        # 算好三角形的三个顶点
        path.moveTo(rect.width() / 2, rect.top())  # 顶部顶点
        path.lineTo(rect.left(), rect.bottom())  # 左下角
        path.lineTo(rect.right(), rect.bottom())  # 右下角
        path.closeSubpath()  # 闭合形状
        return path


class CircleWidget(QFWidget):
    def getShapePath(self) -> QPainterPath:
        rect = self.contentsRect()
        path = QPainterPath()
        # 直接在留白区域内画圆
        path.addEllipse(rect)
        return path



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ball = TriangleWidget()
    ball.show()
    sys.exit(app.exec())
