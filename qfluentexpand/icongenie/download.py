#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


import os
import asyncio
import aiohttp
import httpx
from typing import Callable, Optional, Tuple, Dict
from dataclasses import dataclass


@dataclass
class DownloadResult:
    """下载结果数据类"""
    success: bool
    file_path: str = ""
    error: str = ""
    icon_name: str = ""


class AsyncDownloader:
    """
    Material Icons异步下载器
    """

    def __init__(self, save_dir: str = "material_icons"):
        """
        初始化异步下载器

        Args:
            save_dir: 图标保存目录
        """
        self.save_dir = save_dir
        self._create_save_dir()
        self._session: Optional[aiohttp.ClientSession] = None
        self._downloading: Dict[str, asyncio.Event] = {}
        self._library = None

    def _create_save_dir(self) -> None:
        """创建保存目录"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建HTTP会话"""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    def _get_file_path(self, icon_name: str, color: str, size: int) -> str:
        """生成图标文件路径"""
        return os.path.join(self.save_dir, f"{icon_name}_{color}_{size}.svg")

    def _get_icon_url(self, icon_name: str) -> str:
        """生成图标下载URL"""
        pass

    def setLibrary(self, library: str):
        self._library = library

    async def download(self,
                       icon_name: str,
                       color: str = "black",
                       size: int = 24
                       ) -> DownloadResult:
        """
        异步下载图标

        Args:
            icon_name: 图标名称
            color: 图标颜色
            size: 图标大小

        Returns:
            DownloadResult: 下载结果对象
        """
        file_path = self._get_file_path(icon_name.replace(':', '-'), color, size)
        task_key = f"{icon_name}_{color}_{size}"

        # 检查文件是否已存在
        if os.path.exists(file_path):
            return DownloadResult(True, file_path, icon_name=icon_name)

        # 检查是否已有下载任务
        if task_key in self._downloading:
            await self._downloading[task_key].wait()
            if os.path.exists(file_path):
                return DownloadResult(True, file_path, icon_name=icon_name)

        # 创建下载事件
        download_event = asyncio.Event()
        self._downloading[task_key] = download_event

        try:
            session = await self._get_session()
            url = self._get_icon_url(icon_name)
            params = {"color": color, "size": size}
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(file_path, 'wb') as f:
                        f.write(content)
                    return DownloadResult(True, file_path, icon_name=icon_name)
                else:
                    return DownloadResult(
                        False,
                        error=f"HTTP错误: {response.status}",
                        icon_name=icon_name
                    )

        except Exception as e:
            return DownloadResult(False, error=str(e), icon_name=icon_name)

        finally:
            download_event.set()
            del self._downloading[task_key]

    async def close(self):
        """关闭下载器"""
        if self._session:
            await self._session.close()
            self._session = None


class AsyncIconifyDownloader(AsyncDownloader):
    """
    Iconify异步下载器
    """

    def __init__(self, save_dir: str = "material_icons"):
        """
        初始化异步下载器

        Args:
            save_dir: 图标保存目录
        """
        super().__init__(save_dir)
        self._library = "material-symbols"

    def _get_icon_url(self, name: str) -> str:
        """生成图标下载URL
            备用：
            https://api.simplesvg.com
            https://api.unisvg.com
        """
        tmp = name.split(':')
        if len(tmp) == 2:
            library = tmp[0]
            icon_name = tmp[1]
        else:
            library = self._library
            icon_name = tmp[0]

        return f"https://api.iconify.design/{library}/{icon_name}.svg"

    async def close(self):
        """关闭下载器"""
        if self._session:
            await self._session.close()
            self._session = None


class AsyncGoogleDownloader(AsyncDownloader):
    """
    Material Icons异步下载器
    """

    def _get_icon_url(self, icon_name: str) -> str:
        """生成图标下载URL"""
        return f"https://api.iconify.design/material-symbols/{icon_name}.svg"


class AsyncSimpleIconsDownloader(AsyncDownloader):
    """
    Simple Icons异步下载器
    """

    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建HTTP会话"""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    def _get_icon_url(self, icon_name: str, color_code: str) -> str:
        """生成图标下载URL"""
        return f"https://cdn.simpleicons.org/{icon_name}/{color_code.lstrip('#')}"

    async def download(self,
                       icon_name: str,
                       color: str = "black",
                       size: int = 24
                       ) -> DownloadResult:

        file_path = self._get_file_path(icon_name, color, size)
        task_key = f"{icon_name}_{color}_{size}"

        # 检查文件是否已存在
        if os.path.exists(file_path):
            return DownloadResult(True, file_path, icon_name=icon_name)

        url = self._get_icon_url(icon_name, color)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    content = response.read()
                    with open(file_path, 'wb') as f:
                        f.write(content)
                    return DownloadResult(True, file_path, icon_name=icon_name)
                else:
                    return DownloadResult(
                        False,
                        error=f"HTTP错误: {response.status_code}",
                        icon_name=icon_name
                    )
        except Exception as e:
            return DownloadResult(False, error=str(e), icon_name=icon_name)



