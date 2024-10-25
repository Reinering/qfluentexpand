#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from .base import GoogleMaterialIconBase
from .manager import QFluentManager


class QFluentIcon():

    @classmethod
    def googleIcon(cls, name):
        try:
            name = name.upper()
            GoogleMaterialIconBase.get(name)
            return getattr(GoogleMaterialIconBase, name)
        except AttributeError as e:
            print(e)
            if QFluentManager.google.download(name.lower()):
                return ''
            else:
                return ''
