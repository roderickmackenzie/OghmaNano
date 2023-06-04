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

## @package parasitic
#  Window to edit the parasitic components
#


from tab import tab_class
from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget
from PySide2.QtGui import QPainter,QIcon


from QWidgetSavePos import QWidgetSavePos
from help import help_window
from cal_path import sim_paths
from json_root import json_root
from help import QAction_help

class parasitic(QWidgetSavePos):

	def __init__(self):
		QWidgetSavePos.__init__(self,"parasitic")
		self.setFixedSize(900, 600)
		self.setWindowIcon(icon_get("parasitic"))

		self.setWindowTitle2(_("Edit parasitic components")) 
		

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

		data=json_root()
		files=[data.parasitic]
		description=[_("Parasitic components")]


		for i in range(0,len(files)):
			tab=tab_class(files[i])
			self.notebook.addTab(tab,description[i])


		self.setLayout(self.main_vbox)
		
		json_root().add_call_back(self.update_values)
		self.destroyed.connect(self.doSomeDestruction)

	def doSomeDestruction(self):
		json_root().remove_call_back(self.update_values)

	def update_values(self):
		data=json_root()
		for i in range(0,self.notebook.count()):
			w=self.notebook.widget(i)
			w.tab.template_widget=data.parasitic
			w.tab.update_values()


