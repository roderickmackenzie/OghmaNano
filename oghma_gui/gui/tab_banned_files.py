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

## @package tab_banned_files
#  A window to list files which will not be written to disk
#

from token_lib import tokens

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar
from PySide2.QtGui import QPainter,QIcon

from g_tab2_bin import g_tab2_bin
from json_c import json_tree_c

class tab_banned_files(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.vbox=QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(32, 32))

		self.vbox.addWidget(toolbar)

		self.tab2 = g_tab2_bin(toolbar=toolbar)
		self.tab2.set_tokens(["banned_enabled","banned_file_name"])
		self.tab2.set_labels([_("Enabled"),_("File or token to ban")])

		self.tab2.json_root_path="dump.banned_files"
		self.tab2.setColumnWidth(1, 400)
		self.tab2.setColumnWidth(2, 100)

		self.tab2.populate()
		self.tab2.changed.connect(self.callback_save)

		self.vbox.addWidget(self.tab2)

		self.setLayout(self.vbox)


	def callback_save(self):
		self.bin.save()

class tab_noise(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.vbox=QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(32, 32))

		self.vbox.addWidget(toolbar)

		self.tab2 = g_tab2_bin(toolbar=toolbar)
		self.tab2.set_tokens(["noise_enabled","noise_file_name","noise_sigma"])
		self.tab2.set_labels([_("Enabled"),_("File name"),_("Sigma of noise")])

		self.tab2.json_root_path="dump.noise"
		self.tab2.setColumnWidth(1, 400)
		self.tab2.setColumnWidth(2, 100)
		self.tab2.setColumnWidth(3, 100)
		self.tab2.populate()
		self.tab2.changed.connect(self.callback_save)

		self.vbox.addWidget(self.tab2)

		self.setLayout(self.vbox)


	def callback_save(self):
		self.bin.save()
