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

## @package doping
#  The material gradients window
#

import os
from icon_lib import icon_get

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidgetItem,QAbstractItemView
from PySide2.QtGui import QPainter,QIcon

from open_save_dlg import save_as_image
from QWidgetSavePos import QWidgetSavePos
from cal_path import sim_paths

from error_dlg import error_dlg

from g_tab2_bin import g_tab2_bin
from help import QAction_help
from mesh_math import mesh_math
from json_c import json_tree_c
from bytes2str import str2bytes
from graph import graph_widget
from dat_file import dat_file
import ctypes

class window_material_gradients(QWidgetSavePos):

	def __init__(self):
		QWidgetSavePos.__init__(self,"material_gradients")
		self.bin=json_tree_c()
		self.setMinimumSize(1000, 600)
		self.setWindowIcon(icon_get("doping"))
		self.setWindowTitle2(_("Material gradient editor"))

		self.mesh_y=mesh_math("electrical_solver.mesh.mesh_y")
		self.main_vbox=QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(48, 48))

		self.save = QAction(icon_get("document-save-as"), _("Save"), self)
		self.save.triggered.connect(self.callback_save)
		toolbar.addAction(self.save)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)

		self.canvas2 = graph_widget()
		self.main_vbox.addWidget(self.canvas2)
		self.canvas2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.canvas2.setMinimumSize(400, 400)

		#tab2
		self.tab2 = g_tab2_bin()
		self.tab2.set_tokens(["name","g_x0","g_x1","g_y0","g_y1"])
		self.tab2.set_labels([_("Layer"),"x0 (frac)","x1 (frac)","y0 (frac)","y1 (frac)"])
		self.tab2.json_root_path="epitaxy"
		self.tab2.setColumnWidth(1, 120)
		self.tab2.setColumnWidth(2, 120)
		self.tab2.setColumnWidth(3, 120)
		self.tab2.setColumnWidth(4, 120)
		self.tab2.setColumnWidth(5, 140)
		self.tab2.menu_disabled=True
		self.tab2.check_enabled_callback=self.check_enabled
		self.tab2.populate()
		self.tab2.changed.connect(self.callback_save)

		self.g_x=dat_file()
		self.g_y=dat_file()

		self.main_vbox.addWidget(self.tab2)
		self.update()

		self.setLayout(self.main_vbox)

	def update(self):
		self.draw_graph()


	def draw_graph(self):
		self.g_x_enabled=True
		self.g_y_enabled=True

		if self.g_x_enabled==True:
			self.bin.lib.ui_project_val_to_mesh(ctypes.byref(self.g_x), ctypes.c_char_p(str2bytes("")), ctypes.c_char_p(str2bytes("g_x0")), ctypes.c_char_p(str2bytes("g_x1")), ctypes.byref(self.bin))

		if self.g_y_enabled==True:
			self.bin.lib.ui_project_val_to_mesh(ctypes.byref(self.g_y), ctypes.c_char_p(str2bytes("")), ctypes.c_char_p(str2bytes("g_y0")), ctypes.c_char_p(str2bytes("g_y1")), ctypes.byref(self.bin))

		self.g_x.data_label=b"Material fraction x"
		self.g_x.data_units=b"au"

		self.g_y.data_label=b"Material fraction y"
		self.g_y.data_units=b"au"

		self.canvas2.graph.show_key=True
		self.canvas2.load([self.g_x,self.g_y])
		self.canvas2.update()


	def callback_save(self):
		self.update()
		self.bin.save()

	def check_enabled(self,json_path,token):
		enabled=self.bin.get_token_value(json_path+".shape_dos","enabled")
		if enabled==False:
			return False
		if token=="name":
			return False

		return True

