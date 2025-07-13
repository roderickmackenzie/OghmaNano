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

## @package tab_ml_network
#  The scan tab widget rewritten to use json
#

import os
from g_open import g_open
from icon_lib import icon_get

#qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QDialog,QAction,QStatusBar, QTabWidget

#window
from error_dlg import error_dlg
from g_tab2_bin import g_tab2_bin

import i18n
_ = i18n.language.gettext

from help import help_window
from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos

from decode_inode import decode_inode
from css import css_apply

import platform
from config_window import class_config_window
from cal_path import sim_paths
from json_c import json_tree_c

class tab_ml_network(QWidgetSavePos):

	def cell_changed(self):
		self.callback_save()

	def __init__(self,json_path,uid):
		QWidgetSavePos.__init__(self,"scan_tab")
		self.bin=json_tree_c()
		self.json_path=json_path
		self.uid=uid
		path=self.refind_json_path()
		self.notebook=QTabWidget()
		self.setWindowTitle(_("Neural network editor"))
		self.setWindowIcon(icon_get("neural_network"))

		self.main_vbox = QVBoxLayout()

		self.scan_tab_vbox = QVBoxLayout()

		self.status_bar=QStatusBar()

		css_apply(self.notebook,"tab_default.css")
		self.notebook.setMovable(True)

		#ml inputs
		inputs_toolbar=QToolBar()
		self.scan_tab_vbox.addWidget(inputs_toolbar)

		self.ml_inputs = g_tab2_bin(toolbar=inputs_toolbar)
		self.ml_inputs.set_tokens(["ml_input_vector"])
		self.ml_inputs.set_labels([_("ML Input vector")])
		self.ml_inputs.json_root_path="ml"
		self.ml_inputs.uid=self.uid
		self.ml_inputs.json_postfix="ml_network_inputs"
		self.ml_inputs.fixup_new_row=self.fixup_new_row_inputs
		self.ml_inputs.setColumnWidth(0, 700)
		self.ml_inputs.populate()
		self.ml_inputs.changed.connect(self.cell_changed)
		self.ml_inputs.new_row_clicked.connect(self.add_line)
		self.scan_tab_vbox.addWidget(self.ml_inputs)

		#ml outputs
		outputs_toolbar=QToolBar()
		self.scan_tab_vbox.addWidget(outputs_toolbar)

		self.ml_outputs = g_tab2_bin(toolbar=outputs_toolbar)
		self.ml_outputs.set_tokens(["ml_output_vector"])
		self.ml_outputs.set_labels([_("ML Output vector")])
		self.ml_outputs.json_root_path="ml"
		self.ml_outputs.uid=self.uid
		self.ml_outputs.json_postfix="ml_network_outputs"
		self.ml_outputs.fixup_new_row=self.fixup_new_row_outputs
		self.ml_outputs.setColumnWidth(0, 700)
		self.ml_outputs.populate()
		self.ml_outputs.changed.connect(self.cell_changed)
		self.ml_outputs.new_row_clicked.connect(self.add_line)
		self.scan_tab_vbox.addWidget(self.ml_outputs)

		self.program_widget=QWidget()
		self.program_widget.setLayout(self.scan_tab_vbox)
		self.notebook.addTab(self.program_widget,"Vectors")

		self.notebook.setMinimumSize(1000,500)

		self.main_vbox.addWidget(self.notebook)

		self.main_vbox.addWidget(self.status_bar)		
		self.setLayout(self.main_vbox)

		name=self.bin.get_token_value(path,"name")
		print(name,path,"name")
		self.status_bar.showMessage(sim_paths.get_sim_path()+"("+name+")")

	def add_line(self,data):
		help_window().help_set_help("list-add.png",_("<big><b>The scan window</b></big><br> Now using the drop down menu in the prameter to change 'column', select the device parameter you wish to vary, an example may be dos0/Electron Mobility. Now enter the values you would like it to scan oveer in the  'Values', an example could be '1e-3 1e-4 1e-5 1e-6'.  And hit the double arrorw to run the simulation."))

	def fixup_new_row_inputs(self,row):
		self.ml_inputs.cellWidget(row, 0).refresh(self.uid)
	
	def fixup_new_row_outputs(self,row):
		self.ml_outputs.cellWidget(row, 0).uid=self.uid

	def callback_save(self):
		self.bin.save()

	def callback_menu_tb_optimizer(self):
		path=self.refind_json_path()
		self.mesh_config=class_config_window([path+".scan_optimizer"],[_("Optimizer")],title=_("Scan - Configure Optimizer"),icon="optimizer")
		self.mesh_config.show()

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid(self.json_path,self.uid)
		return ret

