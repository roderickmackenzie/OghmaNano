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

## @package ref
#  Reference manager window.
#


from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView,QPushButton, QTextEdit
from PySide2.QtGui import QPainter,QIcon

#windows

from tab import tab_class

from QWidgetSavePos import QWidgetSavePos
from QWidgetSavePos import resize_window_to_be_sane
from help import QAction_help
from json_c import json_c

class ref_window(QWidgetSavePos):
	def __init__(self,bib_file,token,show_toolbar=True,simple_text=""):
		QWidgetSavePos.__init__(self,"ref_window")
		resize_window_to_be_sane(self,0.4,0.4)
		self.bin=json_c("file_defined")
		
		self.setWindowIcon(icon_get("ref"))
		self.setWindowTitle2(_("Reference manager"))

		self.vbox=QVBoxLayout()

		self.toolbar=QToolBar()
		self.toolbar.setIconSize(QSize(48, 48))

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)

		self.tb_help = QAction_help()
		self.toolbar.addAction(self.tb_help)

		if show_toolbar==True:
			self.vbox.addWidget(self.toolbar)


		self.button_widget=QWidget()
		self.button_hbox=QHBoxLayout()
		self.button_widget.setLayout(self.button_hbox)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.button_hbox.addWidget(spacer)

		if bib_file!=None:
			self.bin.load(bib_file)
			self.bin.json_py_bib_enforce_citation(token)
			self.tab=tab_class(token,data=self.bin)

		else:
			self.tab = QTextEdit(simple_text)
			self.tab.setReadOnly(True)

			font = self.tab.font()
			font.setPointSize(16)
			self.tab.setFont(font)

		self.tab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.vbox.addWidget(self.tab)

		self.vbox.addWidget(self.button_widget)
		self.setLayout(self.vbox)

	def __del__(self):
		self.bin.free()
