#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from typing import Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPainter
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from qfluentwidgets import (
    CaptionLabel, BodyLabel,
    PushButton, PrimaryPushButton,
    ExpandGroupSettingCard, OptionsSettingCard, ExpandGroupSettingCard,
    PushButton, PrimaryPushButton, DropDownPushButton, PrimaryDropDownPushButton,
    LineEdit,
    RoundMenu
)
from qfluentwidgets.components.settings.setting_card import SettingIconWidget
from qfluentwidgets.components.widgets.combo_box import ComboBox
from qfluentwidgets.components.widgets.switch_button import SwitchButton, IndicatorPosition
from qfluentwidgets.components.widgets.slider import Slider
from qfluentwidgets.components.widgets.button import HyperlinkButton
from qfluentwidgets.common.style_sheet import FluentStyleSheet
from qfluentwidgets.common.config import qconfig, isDarkTheme, ConfigItem, OptionsConfigItem
from qfluentwidgets.common.icon import FluentIconBase

from qfluentexpand.components.combox.combo_box import MSComboBox, MSEComboBox, MSECComboBox
from qfluentexpand.components.line.editor import Line
from qfluentexpand.components.line.selector import FilePathSelector, FolderPathSelector


class SettingCardWidget(QWidget):
    """ Setting card """

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

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.iconLabel = SettingIconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content or '', self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        if not content:
            self.contentLabel.hide()

        # self.setFixedHeight(70 if content else 50)
        self.iconLabel.setFixedSize(16, 16)
        #
        # initialize layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(6, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.hBoxLayout.addWidget(self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addSpacing(16)

        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignLeft)

        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)

        self.contentLabel.setObjectName('contentLabel')
        FluentStyleSheet.SETTING_CARD.apply(self)

    def setTitle(self, title: str):
        """ set the title of card """
        self.titleLabel.setText(title)

    def setContent(self, content: str):
        """ set the content of card """
        self.contentLabel.setText(content)
        self.contentLabel.setVisible(bool(content))
    #
    def setValue(self, value):
        """ set the value of config item """
        pass

    def setIconSize(self, width: int, height: int):
        """ set the icon fixed size """
        self.iconLabel.setFixedSize(width, height)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget, 0, Qt.AlignmentFlag.AlignRight)

    def addSpacing(self, spacing):
        self.hBoxLayout.addSpacing(spacing)

    def addStretch(self, stretch):
        self.hBoxLayout.addStretch(stretch)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))
            painter.setPen(QColor(0, 0, 0, 19))

        # painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class LabelSettingCardWidget(SettingCardWidget):
    """ Setting card with Label """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.label = CaptionLabel(self)
        self.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()


class LineSettingCardWidget(SettingCardWidget):
    """ Setting card with CaptionLabel """

    textChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.line = LineEdit(self)
        self.line.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.line.setReadOnly(True)
        self.line.textChanged.connect(self._textChanged)
        self.addWidget(self.line)

    def setText(self, text):
        self.line.setText(text)

    def text(self):
        return self.line.text()

    def _textChanged(self, text):
        self.textChanged.emit(text)


class PushSettingCardWidget(SettingCardWidget):
    """ Setting card with Push Button """

    clicked = Signal()

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button = PushButton(self)
        self.button.clicked.connect(self.On_button_clicked)
        self.addWidget(self.button)

    def setButtonText(self, text):
        self.button.setText(text)

    def setButtonIcon(self, icon):
        self.button.setIcon(icon)

    def On_button_clicked(self):
        self.clicked.emit()


class PrimaryPushSettingCardWidget(SettingCardWidget):
    """ Setting card with Primary Push Button """

    clicked = Signal()

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button = PrimaryPushButton(self)
        self.button.clicked.connect(self.On_button_clicked)
        self.addWidget(self.button)

    def setButtonText(self, text):
        self.button.setText(text)

    def setButtonIcon(self, icon):
        self.button.setIcon(icon)

    def On_button_clicked(self):
        self.clicked.emit()


class MenuSettingCardWidget(SettingCardWidget):
    """ Setting card with menu Drop Down Push Button """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button = DropDownPushButton(self)
        self.addWidget(self.button)
        self.menu = RoundMenu(self)
        self.button.setMenu(self.menu)

    def setButtonText(self, text):
        self.button.setText(text)

    def setButtonIcon(self, icon):
        self.button.setIcon(icon)

    def addSubAction(self, action):
        self.menu.addAction(action)


class MenuPSettingCardWidget(SettingCardWidget):
    """ Setting card with menu Primary Drop Down Push Button """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button = PrimaryDropDownPushButton(self)
        self.addWidget(self.button)
        self.menu = RoundMenu(self)
        self.button.setMenu(self.menu)

    def setButtonText(self, text):
        self.button.setText(text)

    def setButtonIcon(self, icon):
        self.button.setIcon(icon)

    def addSubAction(self, action):
        self.menu.addAction(action)


class HyperlinkCardWidget(SettingCardWidget):
    """ Setting card with Hyper link Button """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.hyperlink = HyperlinkButton(self)
        self.addWidget(self.hyperlink)

    def setButtonText(self, text):
        self.hyperlink.setText(text)

    def setButtonUrl(self, url):
        self.hyperlink.setUrl(url)


class SwitchSettingCardWidget(SettingCardWidget):
    """ Setting card with Switch Button """

    checkedChanged = Signal(bool)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.switch = SwitchButton(self)
        self.switch.checkedChanged.connect(self.on_WwitchButton_checkedChanged)
        self.addWidget(self.switch)

    def on_WwitchButton_checkedChanged(self, checked):
        self.checkedChanged.emit(checked)

    def getOnText(self):
        return self.switch._onText

    def setOnText(self, text):
        self.switch._onText = text
        self.switch._updateText()

    def getOffText(self):
        return self.switch._offText

    def setOffText(self, text):
        self.switch._offText = text
        self.switch._updateText()

    def isChecked(self):
        return self.switch.isChecked()

    def setChecked(self, isChecked):
        """ set checked state """
        self.switch.setChecked(isChecked)


class RangeSettingCardWidget(SettingCardWidget):
    """ Setting card with Slider """

    valueChanged = Signal(int)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.valueLabel = QLabel(self)
        self.slider = Slider(Qt.Orientation.Horizontal, self)
        self.slider.valueChanged.connect(self.on_slider_ValueChanged)
        self.addWidget(self.valueLabel)
        self.addWidget(self.slider)

    def setSliderSingleStep(self, step):
        self.slider.setSingleStep(step)

    def setSliderValue(self, value):
        self.valueLabel.setNum(value)
        self.valueLabel.adjustSize()
        self.slider.setValue(value)

    def setSliderRange(self, min, max):
        self.slider.setRange(min, max)

    def on_slider_ValueChanged(self, value):
        self.valueLabel.setNum(value)
        self.valueLabel.adjustSize()
        self.valueChanged.emit(value)


class ComboBoxSettingCardWidget(SettingCardWidget):
    """ Setting card with ComboBox """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.comboBox = ComboBox(self)
        self.comboBox.currentTextChanged.connect(self.on_comboBox_currentTextChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)
        self.addWidget(self.comboBox)

    def addItems(self, items):
        self.comboBox.addItems(items)

    def currentIndex(self):
        return self.comboBox.currentIndex()

    def setCurrentIndex(self, index):
        self.comboBox.setCurrentIndex(index)

    def currentText(self):
        return self.comboBox.currentText()

    def setCurrentText(self, text):
        self.comboBox.setCurrentText(text)

    def on_comboBox_currentIndexChanged(self, index):
        self.currentIndexChanged.emit(index)

    def on_comboBox_currentTextChanged(self, text):
        self.currentTextChanged.emit(text)


class MSComboBoxSettingCardWidget(SettingCardWidget):
    """ Setting card with MSComboBox """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.comboBox = MSComboBox(self)
        self.comboBox.currentTextChanged.connect(self.on_comboBox_currentTextChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)
        self.addWidget(self.comboBox)

    def addItems(self, items):
        self.comboBox.addItems(items)

    def currentIndex(self):
        return self.comboBox.currentIndex()

    def setCurrentIndex(self, index):
        self.comboBox.setCurrentIndex(index)

    def currentText(self):
        return self.comboBox.currentText()

    def on_comboBox_currentIndexChanged(self, index):
        self.currentIndexChanged.emit(index)

    def on_comboBox_currentTextChanged(self, text):
        self.currentTextChanged.emit(text)


class MSEComboBoxSettingCardWidget(SettingCardWidget):
    """ Setting card with MSEComboBox """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.comboBox = MSEComboBox(self)
        self.comboBox.currentTextChanged.connect(self.on_comboBox_currentTextChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)
        self.addWidget(self.comboBox)

    def addItems(self, items):
        self.comboBox.addItems(items)

    def currentIndex(self):
        return self.comboBox.currentIndex()

    def setCurrentIndex(self, index):
        self.comboBox.setCurrentIndex(index)

    def currentText(self):
        return self.comboBox.currentText()

    def on_comboBox_currentIndexChanged(self, index):
        self.currentIndexChanged.emit(index)

    def on_comboBox_currentTextChanged(self, text):
        self.currentTextChanged.emit(text)


class MSECComboBoxSettingCardWidget(SettingCardWidget):
    """ Setting card with MSECComboBox """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.comboBox = MSECComboBox(self)
        self.comboBox.currentTextChanged.connect(self.on_comboBox_currentTextChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)
        self.addWidget(self.comboBox)

    def addItems(self, items):
        self.comboBox.addItems(items)

    def currentIndex(self):
        return self.comboBox.currentIndex()

    def setCurrentIndex(self, index):
        self.comboBox.setCurrentIndex(index)

    def currentText(self):
        return self.comboBox.currentText()

    def on_comboBox_currentIndexChanged(self, index):
        self.currentIndexChanged.emit(index)

    def on_comboBox_currentTextChanged(self, text):
        self.currentTextChanged.emit(text)


class FileSettingCardWidget(SettingCardWidget):

    textChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.selector = FilePathSelector(self)
        self.selector.textChanged.connect(self.on_selector_textChanged)
        self.addWidget(self.selector)

    def setFileTypes(self, fileTypes):
        self.selector.setFileTypes(fileTypes)

    def setReadOnly(self, checked):
        self.selector.setReadOnly(checked)

    def text(self):
        return self.selector.text()

    def setText(self, text):
        self.selector.setText(text)

    def on_selector_textChanged(self, text):
        self.textChanged.emit(text)


class FolderSettingCardWidget(SettingCardWidget):

    textChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.selector = FolderPathSelector(self)
        self.selector.textChanged.connect(self.on_selector_textChanged)
        self.addWidget(self.selector)

    def setReadOnly(self, checked):
        self.selector.setReadOnly(checked)

    def text(self):
        return self.selector.text()

    def setText(self, text):
        self.selector.setText(text)

    def on_selector_textChanged(self, text):
        self.textChanged.emit(text)