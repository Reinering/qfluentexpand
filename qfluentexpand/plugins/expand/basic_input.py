#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from base import PluginBase



class BasicInputPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Basic Input)'

