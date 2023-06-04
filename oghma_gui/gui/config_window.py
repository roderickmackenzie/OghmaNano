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

## @package config_window
#  Configuration window.
#

from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget
from PySide2.QtGui import QPainter,QIcon

#python modules

#windows
from tab import tab_class

from gQtCore import gSignal
from global_objects import global_object_run

from inp import inp

from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos

from css import css_apply
from json_root import json_root
from help import QAction_help

class class_config_window(QWidgetSavePos):

	changed = gSignal()

	def callback_tab_changed(self):
		self.changed.emit()

	def __init__(self,files,description,title=_("Configure"),icon="preferences-system",data=json_root()):
		QWidgetSavePos.__init__(self,"config_window")
		self.data=data
		self.toolbar=QToolBar()
		self.toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		self.toolbar.setIconSize(QSize(48, 48))

		self.setFixedSize(900, 600)
		self.setWindowIcon(icon_get(icon))

		self.setWindowTitle2(title)

		self.main_vbox = QVBoxLayout()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)

		self.help = QAction_help()
		self.toolbar.addAction(self.help)

		self.main_vbox.addWidget(self.toolbar)



		self.notebook = QTabWidget()
		css_apply(self.notebook,"tab_default.css")
		self.notebook.setMovable(True)

		self.main_vbox.addWidget(self.notebook)

		if (len(files)>0):
			for i in range(0,len(files)):
				file_name=files[i]
				tab=tab_class(file_name,data=self.data)
				tab.tab.changed.connect(self.callback_tab_changed)
				self.notebook.addTab(tab,description[i])

		self.setLayout(self.main_vbox)




