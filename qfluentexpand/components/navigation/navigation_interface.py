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

    def __init__(self, parent=None, showMenuButton=True, showReturnButton=False, collapsible=True):
        super().__init__(parent=parent, showMenuButton=showMenuButton, showReturnButton=showReturnButton, collapsible=collapsible)


    showMenu = Property(bool, fset=lambda self, value: self.panel.setMenuButtonVisible(value),
                            fget=lambda self: self.panel._isMenuButtonVisible)
    showReturn = Property(bool, fset=lambda self, value: self.panel.setReturnButtonVisible(value),
                              fget=lambda self: self.panel._isReturnButtonVisible)