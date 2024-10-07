#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import Union
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QFrame

from qfluentwidgets.common.icon import FluentIconBase
from qfluentwidgets import (
    CardWidget,
    ExpandGroupSettingCard, PrimaryPushButton, BodyLabel,
    SettingCard,
    ComboBox
)
from qfluentwidgets.common.icon import FluentIcon as FIF
from qfluentwidgets.components.settings.expand_setting_card import GroupSeparator, SpaceWidget

from qfluentexpand.common.stylesheets import StyleSheet
from qfluentexpand.components.line.selector import FilePathSelector


class Card(CardWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.hBoxLayout = QHBoxLayout(self)
        # self.addWidget(self.hBoxLayout)

    # def addWidget(self, widget):
    #     self.add


class SettingGroupCard(ExpandGroupSettingCard):

    def addWidget(self, widget):
        self.addGroupWidget(widget)


class ComboBoxSettingCard(SettingCard):
    """ Setting card with a combo box """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        texts: List[str]
            the text of items

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)

        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.comboBox.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.comboBox.currentTextChanged.connect(self.onCurrentTextChanged)


    def getCurrentIndex(self):
        return self.comboBox.currentIndex()

    def getCurrentText(self):
        return self.comboBox.currentText()

    def setCurrentIndex(self, index):
        self.comboBox.setCurrentIndex(index)

    def setCurrentText(self, text):
        self.comboBox.setCurrentText(text)

    def addItems(self, items):
        self.comboBox.addItems(items)

    def onCurrentIndexChanged(self):
        self.currentIndexChanged.emit(self.comboBox.currentIndex())

    def onCurrentTextChanged(self):
        self.currentTextChanged.emit(self.comboBox.currentText())


class FileSelectorSettingCard(SettingCard):
    """ Setting card with a combo box """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        texts: List[str]
            the text of items

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)

        self.selector = FilePathSelector(self)
        self.hBoxLayout.addWidget(self.selector, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def setText(self, text):
        self.selector.setText(text)

    def setFileTypes(self, fileTypes):
        self.selector.setFileTypes(fileTypes)


class ExpandCard(QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QFrame(self)
        self.view = QFrame(self.scrollWidget)

        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.viewLayout = QVBoxLayout(self.view)

        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # initialize layout
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(0)
        self.scrollLayout.addWidget(self.view)

        # initialize style sheet
        self.view.setObjectName('view')
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.EXPAND_CARD.apply(self)

    def wheelEvent(self, e):
        pass

    def resizeEvent(self, e):
        self.scrollWidget.resize(self.width(), self.scrollWidget.height())

        vh = self.viewLayout.sizeHint().height()
        h = self.viewportMargins().top()
        self.setFixedHeight(max(h + vh - self.verticalScrollBar().value(), h))

    def setValue(self, value):
        """ set the value of config item """
        pass

    def addWidget(self, widget: QWidget):
        """ add widget to group """
        # add separator
        if self.viewLayout.count() >= 1:
            self.viewLayout.addWidget(GroupSeparator(self.view))

        widget.setParent(self.view)
        self.viewLayout.addWidget(widget)