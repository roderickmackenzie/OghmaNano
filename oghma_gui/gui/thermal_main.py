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

## @package thermal_main
#  The main thermal dialog.
#

import os
from tab import tab_class
from global_objects import global_object_register

#qt5
from PySide2.QtWidgets import  QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QTabWidget,QStatusBar

#windows
from global_objects import global_object_register
from icon_lib import icon_get

from css import css_apply

from cal_path import sim_paths

from help import QAction_help
from json_c import json_tree_c
from ribbon_page import ribbon_page
from QAction_lock import QAction_lock
from global_objects import global_object_run

class thermal_main(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.setMinimumSize(1000, 600)

		self.main_vbox = QVBoxLayout()

		self.setWindowIcon(icon_get("thermal_kappa"))

		self.setWindowTitle(_("Thermal parameter editor")) 

		self.build_toolbar()

		self.notebook = QTabWidget()

		css_apply(self,"tab_default.css")

		self.main_vbox.addWidget(self.notebook)
		self.setLayout(self.main_vbox)

		self.status_bar=QStatusBar()

		self.main_vbox.addWidget(self.status_bar)	
		self.update()
		self.notebook.currentChanged.connect(self.update_buttons)

	def build_toolbar(self):
		toolbar=ribbon_page()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		self.thermal_enabled = QAction_lock("thermal-off", _("Thermal\neffects"), self,"ribbon_thermal_settemp",icon_pressed="thermal-on")
		self.thermal_enabled.setCheckable(True)
		self.thermal_enabled.clicked.connect(self.callback_buttons)
		toolbar.addAction(self.thermal_enabled)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		toolbar.addWidget(spacer)

		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)


	def update(self):
		self.notebook.clear()

		segments=self.bin.get_token_value("epitaxy","segments")
		for l in range(0,segments):
			path="epitaxy.segment"+str(l)
			if self.bin.get_token_value("electrical_solver","solver_type")!="circuit":
				name=self.bin.get_token_value(path,"name")
				optical_material=self.bin.get_token_value(path,"optical_material")
				uid=self.bin.get_token_value(path,"id")
				db_json_file=os.path.join(sim_paths.get_materials_path(),optical_material,"data.json")
				db_json_sub_path="thermal_constants"
				widget=tab_class("epitaxy",uid=uid,db_json_file=db_json_file,db_json_db_path=db_json_sub_path, json_postfix="shape_heat")

				self.notebook.addTab(widget,name)
		self.update_buttons()

	def callback_buttons(self):
		text=self.sender().text()
		tab = self.notebook.currentWidget()
		if tab==None:
			return

		json_path=self.get_json_path(tab.tab.uid)

		if text==_("Thermal\neffects"):
			thermal_enabled=self.thermal_enabled.isChecked()
			self.bin.set_token_value(json_path,"solve_thermal_problem",thermal_enabled)
			self.bin.save()
		self.update_buttons()
		global_object_run("gl_force_redraw")

	def update_buttons(self):
		tab = self.notebook.currentWidget()
		if tab==None:
			return
		json_path=self.get_json_path(tab.tab.uid)
		
		thermal_enabled=self.bin.get_token_value(json_path,"solve_thermal_problem")
		self.thermal_enabled.setChecked(thermal_enabled)


	def get_json_path(self,uid):
		json_path=self.bin.find_path_by_uid("epitaxy",uid)
		if json_path==None:
			json_path=self.bin.find_path_by_uid("world.world_data",uid)
		return json_path
