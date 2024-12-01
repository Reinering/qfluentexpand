#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QColor, QCursor, QMouseEvent
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget




class PageSticky(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isDragged = True
        self.dragging = False  # 标志位，判断是否正在拖动
        self.drag_start_position = QPoint()  # 记录鼠标拖动起始点

    def setDraggable(self, is_draggable: bool):
        self.isDragged = is_draggable

    def getDraggable(self):
        return self.isDragged

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.isDragged:
                self.dragging = True
                self.drag_start_position = QCursor.pos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # 计算新的位置
            new_pos = QCursor.pos() - self.drag_start_position

            # 限制范围在父窗口内
            if self.parent():
                parent_rect = self.parent().rect()
                new_pos.setX(max(0, min(new_pos.x(), parent_rect.width() - self.width())))
                new_pos.setY(max(0, min(new_pos.y(), parent_rect.height() - self.height())))

            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()

    def eventFilter(self, source, event):
        """
         print(f"Event filtered in ParentWidget: {}")
        """
        if event.type() == QMouseEvent.Type.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == QMouseEvent.Type.MouseButtonPress:
            self.mousePressEvent(event)
        elif event.type() == QEvent.Type.Resize:
            self.resizeEvent(event)
        return super().eventFilter(source, event)