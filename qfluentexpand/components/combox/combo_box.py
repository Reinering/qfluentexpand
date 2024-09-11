#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


import sys
from typing import Union, List, Iterable

from PySide6.QtCore import Qt, Signal, QRectF, QPoint, QObject, QEvent
from PySide6.QtGui import QPainter, QCursor, QIcon, QAction, QFont
from PySide6.QtWidgets import (
    QWidget, QWidgetAction, QVBoxLayout, QHBoxLayout,

)

from qfluentwidgets import CheckBox, MenuAnimationType, PushButton, EditableComboBox
from qfluentwidgets.components.widgets.line_edit import LineEdit, LineEditButton, CompleterMenu
from qfluentwidgets.common.animation import TranslateYAnimation
from qfluentwidgets.common.font import setFont
from qfluentwidgets.common.icon import isDarkTheme, FluentIconBase
from qfluentwidgets.common.icon import FluentIcon as FIF
from qfluentwidgets.common.style_sheet import FluentStyleSheet
from qfluentwidgets.components.widgets.combo_box import ComboBoxBase, ComboItem

from .base import Line


class MSComboBox(Line, ComboBoxBase):
    """ Multi Selection combo box """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setUpUi()
        self.setTextMargins(0, 0, 29, 0)

        self.dropButton = LineEditButton(FIF.ARROW_DOWN, self)
        self.dropButton.setFixedSize(30, 25)
        self.dropButton.clicked.connect(self._toggleComboMenu)
        self.hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignRight)

        self.textChanged.connect(self._onComboTextChanged)
        self.returnPressed.connect(self._onReturnPressed)
        FluentStyleSheet.LINE_EDIT.apply(self)

        self.clearButton.clicked.disconnect()
        self.clearButton.clicked.connect(self._onClearButtonClicked)

        self.items = []
        #
        self.selectedItems = []     # 被选择的index
        self.selectedWidgets = []   # del button
        self.widgets = []   # 下拉列表

        self.rowSize = 1

    def setCompleterMenu(self, menu):
        super().setCompleterMenu(menu)

    def setRowSize(self, size: int):
        if size > 0 and size <= len(self.items):
            self.rowSize = size

    def currentText(self):
        return self.text()

    def selectedTexts(self) -> str:
        tmp = []
        for i in self.selectedItems:
            tmp.append(self.items[i].text)
        return tmp

    def setPlaceholderText(self, text: str):
        self._placeholderText = text
        super().setPlaceholderText(text)

    def eventFilter(self, obj, e: QEvent):
        if obj is self:
            if e.type() == QEvent.MouseButtonPress:
                self.isPressed = True
            elif e.type() == QEvent.MouseButtonRelease:
                self.isPressed = False
            elif e.type() == QEvent.Enter:
                self.isHover = True
            elif e.type() == QEvent.Leave:
                self.isHover = False

        return super().eventFilter(obj, e)

    def addItem(self, text, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        item = ComboItem(text, icon, userData)
        self.items.append(item)

    def addItems(self, texts: Iterable[str]):
        self.clear()
        for text in texts:
            self.addItem(text)

    def insertItem(self, index: int, text: str, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        item = ComboItem(text, icon, userData)
        self.items.insert(index, item)

    def removeItem(self, index: int):
        pass

    def itemData(self, index):
        text = None
        try:
            text = self.widgets[index][1].currentText()
        except Exception as e:
            print(e)
        return text

    def itemDatas(self):
        return [self.itemData(index) for index in self.selectedItems]

    def clear(self):
        """ Clears the combobox, removing all items. """

        self.items.clear()
        self.selectedItems.clear()
        self.widgets.clear()

        if self.isReadOnly():
            for widget in self.selectedWidgets:
                self.hBoxLayout.removeItem(widget)
                widget.deleteLater()
            self.selectedWidgets.clear()

        super().setPlaceholderText(self._placeholderText)

    # 下拉按钮点击事件
    def _toggleComboMenu(self, event):
        if self.dropMenu:
            self._closeComboMenu()
        else:
            self._showComboMenu()

    # 下拉按钮关闭事件
    def _onDropMenuClosed(self):
        if sys.platform != "win32":
            self.dropMenu = None
        else:
            pos = self.mapFromGlobal(QCursor.pos())
            if not self.rect().contains(pos):
                self.dropMenu = None

    def _closeComboMenu(self):
        if not self.dropMenu:
            return

        self.dropMenu.close()
        self.dropMenu = None

    # 生成下拉菜单显示，并绑定事件
    def _showComboMenu(self):
        if not self.items:
            return

        menu = self._createComboMenu()
        self.widgets.clear()
        for i, item in enumerate(self.items):
            if i % self.rowSize == 0:
                tmpWidget = QWidget(menu)
                hBoxLayout = QHBoxLayout(tmpWidget)
                hBoxLayout.setSpacing(1)
                hBoxLayout.setContentsMargins(1, 1, 1, 1)
                menu.addWidget(tmpWidget)

            checkbox = CheckBox()
            # checkbox.setMaximumSize(29, 20)
            checkbox.setMaximumHeight(20)
            checkbox.setObjectName("Checkbox_C_" + str(i))

            if i in self.selectedItems:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

            if item.text:
                checkbox.setText(item.text)

            checkbox.stateChanged.connect(lambda state, index=i: self._onItemChecked(state, index))
            hBoxLayout.addWidget(checkbox)

            tmpWidget.resize(menu.width(), 45)

            self.widgets.append(checkbox)

        if menu.view.width() < self.width():
            menu.view.setMinimumWidth(self.width())
            menu.adjustSize()

        menu.setMaxVisibleItems(self.maxVisibleItems())
        menu.closedSignal.connect(self._onDropMenuClosed)
        self.dropMenu = menu

        x = -menu.width() // 2 + menu.layout().contentsMargins().left() + self.width() // 2
        pd = self.mapToGlobal(QPoint(x, self.height()))
        hd = menu.view.heightForAnimation(pd, MenuAnimationType.DROP_DOWN)

        pu = self.mapToGlobal(QPoint(x, 0))
        hu = menu.view.heightForAnimation(pu, MenuAnimationType.PULL_UP)

        if hd >= hu:
            menu.view.adjustSize(pd, MenuAnimationType.DROP_DOWN)
            menu.exec(pd, aniType=MenuAnimationType.DROP_DOWN)
        else:
            menu.view.adjustSize(pu, MenuAnimationType.PULL_UP)
            menu.exec(pu, aniType=MenuAnimationType.PULL_UP)

    def _onItemTextChanged(self, text, index):
        self.items[index].userData = text

    def _onItemChecked(self, checked, index):
        checked = self.widgets[index].isChecked()
        if checked:
            self.widgets[int(index)].setEnabled(True)

            self.selectedItems.append(index)
            if self.isReadOnly():
                self._addDeleteButton(index, self.items[int(index)].text)
                if len(self.selectedItems) == 1:
                    super().setPlaceholderText('')
        else:
            self.widgets[int(index)].setEnabled(False)

            self.selectedItems.remove(index)
            if self.isReadOnly():
                delButton = self.findChild(PushButton, "DeleteButton_C_" + str(index))
                if delButton:
                    self._removeDelButton(delButton)
                if len(self.selectedItems) == 0:
                    super().setPlaceholderText(self._placeholderText)

    def _addDeleteButton(self, index, text):
        delButton = PushButton(FIF.CLOSE, text)
        delButton.setObjectName("DeleteButton_C_" + str(index))
        delButton.clicked.connect(lambda check, index=index, text=text: self._onDeleteButtonClicked(index, text))

        insert_position = 0
        for i, widget in enumerate(self.selectedWidgets):
            current_index = int(widget.objectName().split('_')[-1])
            if current_index > index:
                break
            insert_position = i + 1

        self.hBoxLayout.insertWidget(insert_position, delButton, 0, Qt.AlignLeft)
        self.selectedWidgets.insert(insert_position, delButton)

    def _removeDelButton(self, widget):
        self.selectedWidgets.remove(widget)
        self.hBoxLayout.removeWidget(widget)
        widget.deleteLater()

    def _onDeleteButtonClicked(self, index, text):
        self.widgets[int(index)].setEnabled(False)

        delButton = self.findChild(PushButton, "DeleteButton_C_" + str(index))
        if delButton:
            self._removeDelButton(delButton)
            self.selectedItems.remove(index)
        if len(self.selectedWidgets) == 0:
            super().setPlaceholderText(self._placeholderText)

    def _onReturnPressed(self):
        if self.isReadOnly() or not self.text():
            return

        index = self.findText(self.text())
        if index >= 0 and index != self.currentIndex():
            self._currentIndex = index
            self.currentIndexChanged.emit(index)
        elif index == -1:
            self.addItem(self.text())
            self.setCurrentIndex(self.count() - 1)

    def _onComboTextChanged(self, text: str):
        if self.isReadOnly():
            return

        self.currentTextChanged.emit(text)

    def _onClearButtonClicked(self):
        if self.isReadOnly():
            self.clear()
        else:
            LineEdit.clear(self)


class MSEComboBox(Line, ComboBoxBase):
    """ Multi Selection Editable combo box """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setUpUi()
        self.setTextMargins(0, 0, 29, 0)

        self.dropButton = LineEditButton(FIF.ARROW_DOWN, self)
        self.dropButton.setFixedSize(30, 25)
        self.dropButton.clicked.connect(self._toggleComboMenu)
        self.hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignRight)

        self.textChanged.connect(self._onComboTextChanged)
        self.returnPressed.connect(self._onReturnPressed)
        FluentStyleSheet.LINE_EDIT.apply(self)

        self.clearButton.clicked.disconnect()
        self.clearButton.clicked.connect(self._onClearButtonClicked)

        self.items = []
        #
        self.selectedItems = []
        self.selectedWidgets = []
        self.widgets = []

        self.rowSize = 1

    def setCompleterMenu(self, menu):
        super().setCompleterMenu(menu)

    def setRowSize(self, size):
        self.rowSize = size

    def currentText(self):
        return self.text()

    def setPlaceholderText(self, text: str):
        self._placeholderText = text
        super().setPlaceholderText(text)

    def eventFilter(self, obj, e: QEvent):
        if obj is self:
            if e.type() == QEvent.MouseButtonPress:
                self.isPressed = True
            elif e.type() == QEvent.MouseButtonRelease:
                self.isPressed = False
            elif e.type() == QEvent.Enter:
                self.isHover = True
            elif e.type() == QEvent.Leave:
                self.isHover = False

        return super().eventFilter(obj, e)

    def addItem(self, text, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        item = ComboItem(text, icon, userData)
        self.items.append(item)

    def addItems(self, texts: Iterable[str]):
        self.clear()
        for text in texts:
            self.addItem(text)

    def insertItem(self, index: int, text: str, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        item = ComboItem(text, icon, userData)
        self.items.insert(index, item)

    def removeItem(self, index: int):
        pass

    def itemData(self, index):
        text = None
        try:
            text = self.widgets[index][1].currentText()
        except Exception as e:
            print(e)
        return text

    def itemDatas(self):
        return [self.itemData(index) for index in self.selectedItems]

    def clear(self):
        """ Clears the combobox, removing all items. """

        self.items.clear()
        self.selectedItems.clear()
        self.widgets.clear()

        if self.isReadOnly():
            for widget in self.selectedWidgets:
                self.hBoxLayout.removeItem(widget)
                widget.deleteLater()
            self.selectedWidgets.clear()

        super().setPlaceholderText(self._placeholderText)

    # 下拉按钮点击事件
    def _toggleComboMenu(self, event):
        if self.dropMenu:
            self._closeComboMenu()
        else:
            self._showComboMenu()

    # 下拉按钮关闭事件
    def _onDropMenuClosed(self):
        if sys.platform != "win32":
            self.dropMenu = None
        else:
            pos = self.mapFromGlobal(QCursor.pos())
            if not self.rect().contains(pos):
                self.dropMenu = None

    def _closeComboMenu(self):
        if not self.dropMenu:
            return

        self.dropMenu.close()
        self.dropMenu = None

    # 生成下拉菜单显示，并绑定事件
    def _showComboMenu(self):
        if not self.items:
            return

        menu = self._createComboMenu()
        self.widgets.clear()

        for i, item in enumerate(self.items):
            tmpWidget = QWidget(menu)

            if i % self.rowSize == 0:
                hBoxLayout = QHBoxLayout(tmpWidget)
                hBoxLayout.setSpacing(1)
                hBoxLayout.setContentsMargins(1, 1, 1, 1)

            checkbox = CheckBox()
            checkbox.setMaximumSize(29, 20)
            checkbox.setObjectName("Checkbox_C_" + str(i))
            lineEdit = LineEdit(menu)
            lineEdit.resize(100, 20)
            lineEdit.setPlaceholderText("{}: 请输入".format(item.text))
            lineEdit.setObjectName("LineEdit_L_" + str(i))

            if i in self.selectedItems:
                checkbox.setChecked(True)
                lineEdit.setEnabled(True)
            else:
                checkbox.setChecked(False)
                lineEdit.setEnabled(False)

            if item.userData:
                lineEdit.setText(item.userData)

            checkbox.stateChanged.connect(lambda state, index=i: self._onItemChecked(state, index))
            lineEdit.textChanged.connect(lambda text, index=i: self._onItemTextChanged(text, index))
            hBoxLayout.addWidget(checkbox)
            hBoxLayout.addWidget(lineEdit)

            tmpWidget.resize(menu.width(), 45)

            menu.addWidget(tmpWidget)

            tmpList = []
            tmpList.append(checkbox)
            tmpList.append(lineEdit)
            self.widgets.append(tmpList)

        if menu.view.width() < self.width():
            menu.view.setMinimumWidth(self.width())
            menu.adjustSize()

        menu.setMaxVisibleItems(self.maxVisibleItems())
        menu.closedSignal.connect(self._onDropMenuClosed)
        self.dropMenu = menu

        x = -menu.width()//2 + menu.layout().contentsMargins().left() + self.width()//2
        pd = self.mapToGlobal(QPoint(x, self.height()))
        hd = menu.view.heightForAnimation(pd, MenuAnimationType.DROP_DOWN)

        pu = self.mapToGlobal(QPoint(x, 0))
        hu = menu.view.heightForAnimation(pu, MenuAnimationType.PULL_UP)

        if hd >= hu:
            menu.view.adjustSize(pd, MenuAnimationType.DROP_DOWN)
            menu.exec(pd, aniType=MenuAnimationType.DROP_DOWN)
        else:
            menu.view.adjustSize(pu, MenuAnimationType.PULL_UP)
            menu.exec(pu, aniType=MenuAnimationType.PULL_UP)

    def _onItemTextChanged(self, text, index):
        self.items[index].userData = text

    def _onItemChecked(self, checked, index):
        checked = self.widgets[index][0].isChecked()
        if checked:
            self.widgets[int(index)][1].setEnabled(True)

            self.selectedItems.append(index)
            if self.isReadOnly():
                self._addDeleteButton(index, self.items[int(index)].text)
                if len(self.selectedItems) == 1:
                    super().setPlaceholderText('')
        else:
            self.widgets[int(index)][1].setEnabled(False)

            self.selectedItems.remove(index)
            if self.isReadOnly():
                delButton = self.findChild(PushButton, "DeleteButton_C_" + str(index))
                if delButton:
                    self._removeDelButton(delButton)
                if len(self.selectedItems) == 0:
                    super().setPlaceholderText(self._placeholderText)

    def _addDeleteButton(self, index, text):
        delButton = PushButton(FIF.CLOSE, text)
        delButton.setObjectName("DeleteButton_C_" + str(index))
        delButton.clicked.connect(lambda check, index=index, text=text: self._onDeleteButtonClicked(index, text))

        insert_position = 0
        for i, widget in enumerate(self.selectedWidgets):
            current_index = int(widget.objectName().split('_')[-1])
            if current_index > index:
                break
            insert_position = i + 1

        self.hBoxLayout.insertWidget(insert_position, delButton, 0, Qt.AlignLeft)
        self.selectedWidgets.insert(insert_position, delButton)

    def _removeDelButton(self, widget):
        self.selectedWidgets.remove(widget)
        self.hBoxLayout.removeWidget(widget)
        widget.deleteLater()

    def _onDeleteButtonClicked(self, index, text):
        self.widgets[int(index)][1].setEnabled(False)

        delButton = self.findChild(PushButton, "DeleteButton_C_" + str(index))
        if delButton:
            self._removeDelButton(delButton)
            self.selectedItems.remove(index)
        if len(self.selectedWidgets) == 0:
            super().setPlaceholderText(self._placeholderText)

    def _onReturnPressed(self):
        if self.isReadOnly() or not self.text():
            return

        index = self.findText(self.text())
        if index >= 0 and index != self.currentIndex():
            self._currentIndex = index
            self.currentIndexChanged.emit(index)
        elif index == -1:
            self.addItem(self.text())
            self.setCurrentIndex(self.count() - 1)

    def _onComboTextChanged(self, text: str):
        if self.isReadOnly():
            return

        self.currentTextChanged.emit(text)

    def _onClearButtonClicked(self):
        if self.isReadOnly():
            self.clear()
        else:
            LineEdit.clear(self)


class MSECComboBox(MSEComboBox):
    """ Multi Selection Editable Cache combo box """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextMargins(0, 0, 29, 0)
        FluentStyleSheet.LINE_EDIT.apply(self)

        self.widgets = {}

    def addItem(self, text: str, datas: list, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        item = ComBoxItem(text, datas, icon, userData)
        self.items.append(item)

    def addItems(self, datas: Iterable[dict]):
        self.clear()
        for key, value in datas.items():
            self.addItem(key, value)

    def insertItem(self, index: int, text: str, datas: list, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        item = ComBoxItem(text, datas, icon, userData)
        self.items.insert(index, item)

    def removeItem(self, index: int):
        pass

    def itemData(self, key):
        text = None
        try:
            text = self.widgets[key][1].currentText()
        except Exception as e:
            print(e)
        return text

    def itemDatas(self):
        return {key: self.itemData(key) for key in self.selectedItems}

    def setItemReadOnly(self, key, enabled: bool):
        for item in self.items:
            if item.text == key:
                item.readOnly = enabled

    def clear(self):
        """ Clears the combobox, removing all items. """

        self.items.clear()
        self.selectedItems.clear()
        self.widgets.clear()

        if self.isReadOnly():
            for widget in self.selectedWidgets:
                self.hBoxLayout.removeItem(widget)
                widget.deleteLater()
            self.selectedWidgets.clear()

        super().setPlaceholderText(self._placeholderText)

    # 生成下拉菜单显示，并绑定事件
    def _showComboMenu(self):
        if not self.items:
            return

        menu = self._createComboMenu()
        self.widgets.clear()
        for i, item in enumerate(self.items):
            tmpWidget = QWidget(menu)

            hBoxLayout = QHBoxLayout(tmpWidget)
            hBoxLayout.setSpacing(1)
            hBoxLayout.setContentsMargins(1, 1, 1, 1)

            checkbox = CheckBox()
            checkbox.setMaximumSize(29, 20)
            checkbox.setObjectName("Checkbox_C_" + str(i))

            combobox = EditableComboBox(menu)
            combobox.resize(100, 20)
            combobox.setPlaceholderText("{}: 请输入".format(item.text))
            combobox.addItems(item.datas)
            combobox.setCurrentIndex(-1)
            combobox.setObjectName("ComboBox_L_" + str(i))

            if item.text in self.selectedItems:
                checkbox.setChecked(True)
                combobox.setEnabled(True)
            else:
                checkbox.setChecked(False)
                combobox.setEnabled(False)

            if item.userData:
                combobox.setText(item.userData)
            if item.readOnly:
                combobox.setReadOnly(True)

            checkbox.stateChanged.connect(lambda state, index=i, key=item.text: self._onItemChecked(state, index, key))
            combobox.textChanged.connect(lambda text, index=i, key=item.text: self._onItemTextChanged(text, index, key))
            hBoxLayout.addWidget(checkbox)
            hBoxLayout.addWidget(combobox)

            tmpWidget.resize(menu.width(), 45)

            menu.addWidget(tmpWidget)

            tmpList = []
            tmpList.append(checkbox)
            tmpList.append(combobox)
            self.widgets[item.text] = tmpList

        if menu.view.width() < self.width():
            menu.view.setMinimumWidth(self.width())
            menu.adjustSize()

        menu.setMaxVisibleItems(self.maxVisibleItems())
        menu.closedSignal.connect(self._onDropMenuClosed)
        self.dropMenu = menu

        x = -menu.width() // 2 + menu.layout().contentsMargins().left() + self.width() // 2
        pd = self.mapToGlobal(QPoint(x, self.height()))
        hd = menu.view.heightForAnimation(pd, MenuAnimationType.DROP_DOWN)

        pu = self.mapToGlobal(QPoint(x, 0))
        hu = menu.view.heightForAnimation(pu, MenuAnimationType.PULL_UP)

        if hd >= hu:
            menu.view.adjustSize(pd, MenuAnimationType.DROP_DOWN)
            menu.exec(pd, aniType=MenuAnimationType.DROP_DOWN)
        else:
            menu.view.adjustSize(pu, MenuAnimationType.PULL_UP)
            menu.exec(pu, aniType=MenuAnimationType.PULL_UP)

    def _onItemTextChanged(self, text, index, key):
        self.items[index].userData = text

    def _onItemChecked(self, checked, index, key):
        checked = self.widgets[key][0].isChecked()

        if checked:
            self.widgets[key][1].setEnabled(True)

            self.selectedItems.append(key)
            if self.isReadOnly():
                self._addDeleteButton(index, key)
                if len(self.selectedItems) == 1:
                    tmp = self._placeholderText
                    self.setPlaceholderText('')
                    self._placeholderText = tmp

        else:
            self.widgets[key][1].setEnabled(False)

            if self.isReadOnly():
                delButton = self.findChild(PushButton, "DeleteButton_C_" + str(index))
                if delButton:
                    self._removeDelButton(delButton)
                    self.selectedItems.remove(key)
                if len(self.selectedItems) == 0:
                    self.setPlaceholderText(self._placeholderText)

    def _addDeleteButton(self, index, text):
        delButton = PushButton(FIF.CLOSE, text)
        delButton.setObjectName("DeleteButton_C_" + str(index))
        delButton.clicked.connect(lambda check, index=index, text=text: self._onDeleteButtonClicked(index, text))

        insert_position = 0
        for i, widget in enumerate(self.selectedWidgets):
            current_index = int(widget.objectName().split('_')[-1])
            if current_index > index:
                break
            insert_position = i + 1

        self.hBoxLayout.insertWidget(insert_position, delButton, 0, Qt.AlignLeft)
        self.selectedWidgets.insert(insert_position, delButton)

    def _removeDelButton(self, widget):
        self.selectedWidgets.remove(widget)
        self.hBoxLayout.removeWidget(widget)
        widget.deleteLater()

    def _onDeleteButtonClicked(self, index, key):
        self.widgets[key][1].setEnabled(False)

        delButton = self.findChild(PushButton, "DeleteButton_C_" + str(index))
        if delButton:
            self._removeDelButton(delButton)
            self.selectedItems.remove(key)

        if len(self.selectedWidgets) == 0:
            self.setPlaceholderText(self._placeholderText)


class ComBoxItem:
    """ Combo box item """

    def __init__(self, text: str, datas: list, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        """ add item

        Parameters
        ----------
        text: str
            the text of item

        icon: str | QIcon | FluentIconBase
            the icon of item

        userData: Any
            user data
        """
        self.text = text
        self.datas = datas
        self.userData = userData
        self.readOnly = False
        self.icon = icon

    @property
    def icon(self):
        if isinstance(self._icon, QIcon):
            return self._icon

        return self._icon.icon()

    @icon.setter
    def icon(self, ico: Union[str, QIcon, FluentIconBase]):
        if ico:
            self._icon = QIcon(ico) if isinstance(ico, str) else ico
        else:
            self._icon = QIcon()