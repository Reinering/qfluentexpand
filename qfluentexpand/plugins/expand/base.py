#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


import re

from PySide6.QtGui import QIcon
from PySide6.QtDesigner import QDesignerFormEditorInterface


class PluginBase:

	Factory = None

	#  这个init必须这么写，不然会报错
	def __init__(self):
		super().__init__()
		self.initialized = False
		self.factory = None
		self.pattern = re.compile(r'(?<!^)(?=[A-Z])')

	def initialize(self, editor: QDesignerFormEditorInterface):
		if self.initialized:
			return

		self.initialized = True
		if not self.Factory:
			return

		manager = editor.extensionManager()
		self.factory = self.Factory(manager)
		manager.registerExtensions(self.factory, self.factory.IID)

	def isInitialized(self):
		return self.initialized

	def icon(self, name: str):
		return QIcon(f":/qfluentexpand/images/controls/{name}.png")

	def name(self):
		return "PluginBase"

	def group(self):
		return "Fluent-Widgets-Expand"

	def toolTip(self):
		name = self.pattern.sub(' ', self.name()).lower()
		return name[0].upper() + name[1:]

	def whatsThis(self):
		return self.toolTip()

	def isContainer(self):
		return False

	def domXml(self):
		return f'<widget class="{self.name()}" name="{self.name()}"></widget>'

	def includeFile(self):
		""""
		package name
		"""
		return "qfluentexpand"
