#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from PySide6.QtGui import QColor
import PySide6 as ref_mod

from enum import Enum
from typing import Union
import os
import sys
import asyncio
import subprocess
import threading
from pathlib import Path

from qfluentwidgets import getIconColor, Theme, FluentIconBase, qconfig

from .download import AsyncGoogleDownloader, AsyncIconifyDownloader, AsyncSimpleIconsDownloader
from .rc import QRC, Resource, QrcParser
from .enum_ import ExtendableEnum


class QFluentIconBase(FluentIconBase):

    def __init__(self):
        super().__init__()
        self.size = 24
        self.servicesProvided = ''
        self.prefix = ':/app'
        self.iconPath = 'icons'
        self.fontPath = 'fonts'

    @classmethod
    def add(cls, name, value):
        setattr(cls, name, value)

    @classmethod
    def get(cls, name):
        getattr(cls, name)


class GoogleMaterialIconBase(QFluentIconBase, ExtendableEnum):

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":{self.prefix}/{self.servicesProvided}/{self.iconPath}/{self.value}_{getIconColor(theme, reverse=False)}_{self.size}.svg"


class IconifyIconBase(QFluentIconBase, ExtendableEnum):

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":{self.prefix}/{self.servicesProvided}/{self.iconPath}/{self.value}_{getIconColor(theme)}_{self.size}.svg"


class SimpleIconsIconBase(QFluentIconBase, ExtendableEnum):

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":{self.prefix}/{self.servicesProvided}/{self.iconPath}/{self.value}_{getIconColor(theme)}_{self.size}.svg"


class IconFontBase():

    def __init__(self):
        super().__init__()
        self.servicesProvided = ''
        self.prefix = '/app'
        self.iconPath = 'icons'
        self.fontPath = 'fonts'
        self.size = 24
        self.icons = []
        self.waitTime = 20
        self.timer = None

        self.root_path = './'
        self.qrcPath = os.path.join(self.root_path, 'resources', 'resource_qfe.qrc')
        self.resourcePath = os.path.join(self.root_path, 'resource_qfe.py')

        self.pyside_dir = Path(ref_mod.__file__).resolve().parent

        self.downloadBlock = False
        self.downloader = None
        self.library = None

    def init(self):
        self.resource = Resource(self.resourcePath)

        # 判断是否打包
        if not getattr(sys, 'frozen', False) and not '__compiled__' in globals():
            self.createFile(self.root_path)
            if not os.path.exists(self.qrcPath):
                QRC.writeQRC(self.qrcPath, '', prefix=self.prefix)
            self.qrc = QrcParser(self.qrcPath)

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

    def setLibrary(self, library: str):
        self.library = library

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

    def rcc1(self):
        async def async_rcc():
            async def compile():
                exe = os.path.join(self.pyside_dir, "rcc")
                cmd = [
                    'pyside6-rcc',
                    '-g',
                    'python',
                    self.qrcPath,
                    '-o',
                    self.resourcePath
                ]
                process = subprocess.run(cmd)
                if process.returncode != 0:
                    command = ' '.join(cmd)
                    print(f"'{command}' returned {process.returncode}", file=sys.stderr)
                else:
                    print("rcc success!")

            await compile()

        asyncio.run(async_rcc())

    def rcc(self):
        exe = os.path.join(self.pyside_dir, "rcc")
        cmd = [
            'pyside6-rcc',
            self.qrcPath,
            '-o',
            self.resourcePath
        ]
        process = subprocess.run(cmd)
        if process.returncode != 0:
            command = ' '.join(cmd)
            print(f"'{command}' returned {process.returncode}", file=sys.stderr)
        else:
            print("rcc success!")

    def download(self, name: Union[str, list], theme=Theme.AUTO, color: QColor = None):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        color = getIconColor(theme, reverse=True)

        async def async_download():
            async def download_icons():
                process = self.downloader(
                    os.path.join(self.root_path, 'resources', self.servicesProvided, self.iconPath))
                process.setLibrary(self.library)

                # 并发下载多个图标
                # icons = [
                #     ("home", "black", 24),
                #     ("search", "#2196F3", 32),
                #     ("favorite", "#E91E63", 28)
                # ]

                tasks = [
                    process.download(icon_name, color, size)
                    for icon_name, color, size in self.icons
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

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
                        QFluentIconBase.add(name1.upper(), name1)
                    else:
                        print(f"图标 {result.icon_name} 下载失败: {result.error}")

                self.icons.clear()
                self.rcc()
                # self.resource.reload()
                # self.setAttr()

                await process.close()

            await download_icons()

        def _run_async(coro):
            """安全地运行异步代码的辅助方法"""
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            return loop.run_until_complete(coro)

        if isinstance(name, str):
            if not os.path.exists(os.path.join(self.root_path, 'resources', self.servicesProvided, self.iconPath,
                                               '_'.join((name, color, str(self.size)))) + '.svg'):
                self.icons.append((name, color, self.size))
        elif isinstance(name, list):
            if len(name) > 0 and (isinstance(name[0], list) or isinstance(name[0], tuple)):
                for n in name:
                    if not os.path.exists(os.path.join(
                            self.root_path, 'resources', self.servicesProvided, self.iconPath, '_'.join((n[0], n[1], str(n[2]))) + '.svg')):
                        self.icons.append(n)
            else:
                if not os.path.exists(os.path.join(
                        self.root_path, 'resources', self.servicesProvided, self.iconPath, '_'.join((name[0], name[1], str(name[2]))) + '.svg')):
                    self.icons.append(name)

        if len(self.icons) > 0 and self.timer is None:
            self.timer = threading.Timer(self.waitTime, lambda: _run_async(async_download()))
            self.timer.start()
            if self.downloadBlock:
                self.timer.join()


class GoogleMaterialBase(IconFontBase):

    def __init__(self):
        super().__init__()
        self.servicesProvided = 'google'
        self.downloader = AsyncGoogleDownloader

    def setSize(self, size):
        self.size = size
        GoogleMaterialIconBase.size = size

    def setAttr(self):
        super().setAttr(GoogleMaterialIconBase)

    def initialize(self):
        super().init()
        if os.path.exists(self.resourcePath):
            self.resource.load()
            self.setAttr()


class IconifyBase(IconFontBase):

    def __init__(self):
        super().__init__()
        self.servicesProvided = 'iconify'
        self.library = "material-symbols"
        self.downloader = AsyncIconifyDownloader

    def setSize(self, size):
        self.size = size
        IconifyIconBase.size = size

    def setAttr(self):
        super().setAttr(IconifyIconBase)

    def initialize(self):
        super().init()
        if os.path.exists(self.resourcePath):
            self.resource.load()
            self.setAttr()


class SimpleIconsBase(IconFontBase):

    def __init__(self):
        super().__init__()
        self.servicesProvided = 'simpleicons'
        self.downloader = AsyncSimpleIconsDownloader

    def setSize(self, size):
        self.size = size
        SimpleIconsIconBase.size = size

    def setAttr(self):
        super().setAttr(SimpleIconsIconBase)

    def initialize(self):
        super().init()
        if os.path.exists(self.resourcePath):
            self.resource.load()
            self.setAttr()







