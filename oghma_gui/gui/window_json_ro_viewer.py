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

## @package window_json_ro_viewer
#  Read only viewer for json files
#


from tab import tab_class
from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget
from PySide2.QtGui import QPainter,QIcon

#python modules

from help import help_window
from help import QAction_help

from QWidgetSavePos import QWidgetSavePos
from inp import inp
from json_base import json_base
class window_json_ro_viewer(QWidgetSavePos):

	def __init__(self,file_name,icon="json_file",title=_("Simulation information")):
		QWidgetSavePos.__init__(self,"info")
		self.setFixedSize(900, 600)
		self.setWindowIcon(icon_get(icon))

		self.setWindowTitle2(title) 
		
		self.main_vbox = QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)


		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)


		self.notebook = QTabWidget()

		self.notebook.setMovable(True)

		self.main_vbox.addWidget(self.notebook)

		self.f=inp()
		self.f.load_json(file_name)
		a=json_base("decode")
		a.import_raw_json(self.f.json)
		tab=tab_class(a)
		tab.set_edit(False)
		self.notebook.addTab(tab,_("Information"))

		self.setLayout(self.main_vbox)



