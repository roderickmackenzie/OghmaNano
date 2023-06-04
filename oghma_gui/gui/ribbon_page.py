# -*- coding: utf-8 -*-
#
#   OghmaNano - Organic and hybrid Material Nano Simulation tool
#   Copyright (C) 2008-2022 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
#
#   https://www.oghma-nano.com
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#   SOFTWARE.
#

## @package ribbon_page
#  The ribbon page
#
#qt
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu
from json_local_root import json_local_root

class ribbon_page(QToolBar):

	def __init__(self):
		QToolBar.__init__(self)

		self.xy_size=json_local_root().gui_config.toolbar_icon_size
		if self.xy_size>24:
			self.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		else:
			self.setToolButtonStyle( Qt.ToolButtonTextBesideIcon)

		self.setIconSize(QSize(self.xy_size, self.xy_size))
		self.setStyleSheet("QToolButton { padding-left: 0px; padding-right: 0px; padding-top: 0px;padding-bottom: 0px; margin: 0;} QToolBar { padding: 0; }")

	def show_window(self,win):
		win.show()
		win.setWindowState(Qt.WindowNoState)

class ribbon_page2(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		
		self.hbox = QHBoxLayout()
		self.hbox.setSpacing(0)
		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.hbox)
		#self.setStyleSheet(" padding-left: 0px; padding-right: 0px; padding-top: 0px;padding-bottom: 0px; margin: 0; border 0px;")

	def add_panel(self):
		t=ribbon_page()
		#t.setIconSize(QSize(42, 42))
		#t.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		#t.setStyleSheet(" padding-left: 0px; padding-right: 0px; padding-top: 0px;padding-bottom: 0px; margin: 0;")
		self.hbox.addWidget(t)
		return t

	def show_window(self,win):
		win.show()
		win.setWindowState(Qt.WindowNoState)
