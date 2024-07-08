#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Property

from qfluentwidgets import NavigationInterface



class Navigation(NavigationInterface):
    """ Navigation interface """

    def __init__(self, showMenuButton=True, showReturnButton=False, collapsible=True, parent=None):
        super().__init__(showMenuButton, showReturnButton, collapsible, parent=parent)


    showMenu = Property(bool, fset=lambda self, value: self.panel.setMenuButtonVisible(value),
                            fget=lambda self: self.panel._isMenuButtonVisible)
    showReturn = Property(bool, fset=lambda self, value: self.panel.setReturnButtonVisible(value),
                              fget=lambda self: self.panel._isReturnButtonVisible)