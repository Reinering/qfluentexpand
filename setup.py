# coding=utf-8
__author__ = 'Reiner'

from setuptools import setup, find_packages

# 读取项目的readme介绍
with open("qfluentexpand/README.md", "r") as fh:
  long_description = fh.read()

setup(
    name="qfluentexpand",
    version="0.0.0",
    author="Reiner",
    author_email="nbxlhc@hotmail.com",
    description="Secondary Encapsulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)
