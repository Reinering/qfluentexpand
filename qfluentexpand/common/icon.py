#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase, qconfig



class APPICON(FluentIconBase, Enum):


    ALL_INBOX = "all_inbox"
    CONTENT_COPY = "content_copy"
    CONTENT_CUT = "content_cut"
    COPY_ALL = "copy_all"
    COPYRIGHT = "copyright"
    DNS = "dns"
    DOCUMENT = "document"
    FILE_COPY = "file_copy"
    FOLDER = "folder"
    FOLDER_COPY = "folder_copy"
    HOME = "home"
    INVENTORY = "inventory"
    PICTURE_AS_PDF = "picture_as_pdf"
    RECEIPT = "receipt"
    SETTINGS = "settings"
    SOURCE = "source"
    TERMINAL = "terminal"


    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f':/qfluentexpand/images/icons/{theme.value.lower()}/{self.value}.svg'
