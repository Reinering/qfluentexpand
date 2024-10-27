#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
import PySide6 as ref_mod

from enum import Enum
from typing import Union
import os
import sys
import asyncio
import subprocess
from pathlib import Path

from qfluentwidgets import getIconColor, Theme, FluentIconBase, qconfig

from .tools import AsyncGoogleDownloader
from .rc import QRC, Resource, QrcParser
from .enum_ import ExtendableEnum



class GoogleMaterialIconBase(FluentIconBase, ExtendableEnum):

    @classmethod
    def add(cls, name, value):
        setattr(cls, name, value)

    @classmethod
    def get(cls, name):
        getattr(cls, name)

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":{self.prefix}/{self.servicesProvided}/{self.iconPath}/{self.value}_{getIconColor(theme, reverse=True)}_{self.size}.svg"


class IconFontBase():

    def __init__(self):
        super().__init__()
        self.servicesProvided = ''
        self.prefix = '/app'
        self.iconPath = 'icons'
        self.fontPath = 'fonts'
        self.size = 24

        self.root_path = './'
        self.qrcPath = os.path.join(self.root_path, 'resources', 'resource_qfe.qrc')
        self.resourcePath = os.path.join(self.root_path, 'resource_qfe.py')

        self.pyside_dir = Path(ref_mod.__file__).resolve().parent

    def init(self):
        self.resource = Resource(self.resourcePath)

        # 判断是否打包
        if not getattr(sys, 'frozen', False) and not '__compiled__' in globals():
            if not os.path.exists(self.qrcPath):
                QRC.writeQRC(self.qrcPath, '', prefix=self.prefix)
            self.qrc = QrcParser(self.qrcPath)
            self.createFile(self.root_path)

    def setSize(self, size):
        self.size = size

    def setRootPath(self, path):
        if not Path.is_dir(Path(path)):
            print(f"Path '{path}' is not a directory", file=sys.stderr)
            return
        self.root_path = path
        self.qrcPath = os.path.join(self.root_path, 'resources', 'resource_qfe.qrc')
        self.resourcePath = os.path.join(self.root_path, 'resource_qfe_rc.py')

    def setQRCPath(self, path):
        self.qrcPath = path

    def setResourcePath(self, path):
        self.resourcePath = path

    def setPrefix(self, prefix):
        self.prefix = prefix

    def getFontPath(self):
        return os.path.join(self.root_path, 'resources', self.servicesProvided, self.fontPath)

    def getIconPath(self):
        return os.path.join(self.root_path, 'resources', self.servicesProvided, self.iconPath)

    def createFile(self, root_dir):
        tmp = os.path.join(root_dir, 'resources')
        if not os.path.exists(tmp):
            os.makedirs(tmp)

        tmp = os.path.join(root_dir, 'resources', self.servicesProvided, self.iconPath)
        if not os.path.exists(tmp):
            os.makedirs(tmp)

    def extend(self, cls, name, value):
        cls.extend(name,
                   value,
                   servicesProvided=self.servicesProvided,
                   iconPath=self.iconPath,
                   size=self.size,
                   prefix=self.prefix
                   )

    def setAttr(self, cls):
        prefix = ':' + os.path.join(self.prefix, self.servicesProvided, self.iconPath)

        images = self.resource.getImages(prefix)
        for img in images:
            (filepath, filename) = os.path.split(img)
            (name, suffix) = os.path.splitext(filename)
            name = name.split('_')[0]
            self.extend(cls, name.upper(), name)

    def rcc(self):
        exe = os.path.join(self.pyside_dir, "rcc")
        cmd = [
            'pyside6-rcc',
            '-g',
            'python',
            self.qrcPath,
            '-o',
            self.resourcePath
        ]
        returncode = subprocess.call(cmd)
        if returncode != 0:
            command = ' '.join(cmd)
            print(f"'{command}' returned {returncode}", file=sys.stderr)

    def download(self):
        pass


class GoogleMaterialBase(IconFontBase):

    def __init__(self):
        super().__init__()
        self.servicesProvided = 'google'
        self.prefix = '/app'
        self.icons = []
        self.waitTime = 20
        self.timer = None

    def setAttr(self):
        super().setAttr(GoogleMaterialIconBase)

    def setSize(self, size):
        self.size = size
        GoogleMaterialIconBase.size = size

    def init(self):
        super().init()
        if os.path.exists(self.resourcePath):
            self.resource.load()
            self.setAttr()

    def download(self, name: Union[str, list], theme=Theme.AUTO, color: QColor = None, size=24):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        color = getIconColor(theme, reverse=True)

        async def async_download():
            async def download_icons():
                downloader = AsyncGoogleDownloader(os.path.join(self.root_path, 'resources', self.servicesProvided, self.iconPath))

                # 并发下载多个图标
                # icons = [
                #     ("home", "black", 24),
                #     ("search", "#2196F3", 32),
                #     ("favorite", "#E91E63", 28)
                # ]

                tasks = [
                    downloader.download(icon_name, color, size)
                    for icon_name, color, size in self.icons
                ]

                results = await asyncio.gather(*tasks)

                for result in results:
                    if result.success:
                        print(f"图标 {result.icon_name} 下载成功: {result.file_path}")
                        name1 = name
                        (filepath, filename) = os.path.split(result.file_path)
                        if not self.qrc.has_icon(os.path.join(self.servicesProvided, self.iconPath, filename),
                                                 check_content=True):
                            self.qrc.add_resource(os.path.join(self.servicesProvided, self.iconPath, filename),
                                                  self.prefix)
                            name1 = filename.split('_')[0]
                        GoogleMaterialIconBase.add(name1.upper(), name1)
                    else:
                        print(f"图标 {result.icon_name} 下载失败: {result.error}")

                self.icons.clear()
                self.rcc()
                self.resource.load()

                await downloader.close()

                # 添加RCC

            await download_icons()

        if isinstance(name, str):
            if not os.path.exists(os.path.join(self.root_path, 'resources', self.servicesProvided, self.iconPath, '_'.join((name, color, str(size)))) + '.svg'):
                self.icons.append((name, color, size))
        elif isinstance(name, list):
            if not os.path.exists(
                    self.root_path, 'resources', os.path.join(self.servicesProvided, self.iconPath, '_'.join(name))):
                self.icons.append(name)

        if len(self.icons) == 1:
            self.timer = QTimer()
            self.timer.singleShot(self.waitTime, lambda: asyncio.run(async_download()))
            self.timer.startTimer(self.waitTime)





