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
from PySide2.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView,QPushButton
from PySide2.QtGui import QPainter,QIcon

#windows

from tab import tab_class

from bibtex import bibtex

from QWidgetSavePos import QWidgetSavePos
from QWidgetSavePos import resize_window_to_be_sane
from help import QAction_help

class ref_window(QWidgetSavePos):
	def __init__(self,bib_file,token,show_toolbar=True):
		"""Pass this the file name of the file you want referenced."""
		QWidgetSavePos.__init__(self,"ref_window")
		resize_window_to_be_sane(self,0.5,0.5)
		self.bib_file=bib_file
		self.token=token
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


		self.b=bibtex()
		self.b.load(self.bib_file)
		self.item=self.b.get_ref(self.token)
		if self.item==False:
			self.item=self.b.new()
			self.item.token=token

		self.tab=tab_class(self.item,data=self.item)
		#self.item.bib_dump()
		self.tab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.vbox.addWidget(self.tab)

		self.vbox.addWidget(self.button_widget)
		self.setLayout(self.vbox)


