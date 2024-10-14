#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
"""
author: Reiner
email: nbxlc@hotmail.com
"""

__author__ = 'Reiner'


from pathlib import Path
# import pkg_resources
# from importlib import resources
from setuptools import setup, find_packages

# 读取项目的readme介绍
with open("qfluentexpand/README.md", "r", encoding="gbk") as fh:
  long_description = fh.read()


def read_version(fname="qfluentexpand/__init__.py"):
    exec(compile(open(fname, encoding="utf-8").read(), fname, "exec"))
    return locals()["__version__"]

setup(
    name="qfluentexpand",
    py_modules=["qfluentexpand"],
    version="0.0.0",
    author=__author__,
    author_email="nbxlhc@hotmail.com",
    description="Secondary Encapsulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Reinering/qfluentexpand.git',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # install_requires=[
    #     str(r)
    #     for r in pkg_resources.parse_requirements(
    #         Path(__file__).with_name("requirements.txt").open()
    #     )
    # ],
    include_package_data=True,
    # scripts=['scripts/designer.bat'],
    # data_files=[
    #     ('scripts', ['tools/designer.bat'])  # 将 designer.bat 安装到 scripts 目录
    # ],

    package_data={
        'qfluentexpand': ['tools/designer-pyside6.bat', 'tools/designer-pyside6.bat'],
    },
    entry_points={
        'console_scripts': [
            # 'designer = qfluentexpand.__main__:main'
            'designer = qfluentexpand.tools.designer:main'
        ]
    }
)
