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

## @package layer_widget
#  The window to select and build the device structure.
#
import os
import i18n
from icon_lib import icon_get
from g_tab2_bin import g_tab2_bin
from PySide2.QtWidgets import QWidget, QSizePolicy, QVBoxLayout ,QToolBar, QStatusBar, QAction, QMenu
from global_objects import global_object_run
from global_objects import global_object_get
from QWidgetSavePos import QWidgetSavePos
from util import distance_with_units
from PySide2.QtGui import QColor
from cal_path import sim_paths
from QColorMap import QColorMap
from mesh_math import mesh_math
from json_c import json_tree_c
import ctypes

_ = i18n.language.gettext

class layer_widget(QWidgetSavePos):

	def __init__(self):
		QWidgetSavePos.__init__(self,"layer_widget")
		self.bin=json_tree_c()
		self.warning=""
		self.setWindowTitle2(_("Layer editor"))
		self.setWindowIcon(icon_get("layers"))
		self.resize(800,500)
		self.mesh_y=mesh_math("electrical_solver.mesh.mesh_y")
		self.main_vbox=QVBoxLayout()

		self.toolbar=QToolBar()

		self.tab2 = g_tab2_bin(toolbar=self.toolbar)
		self.tab2.fixup_new_row=self.fixup_new_row
		self.tab2.set_tokens(["name","dy","optical_material","obj_type","solve_optical_problem","id"])
		self.tab2.set_labels([_("Layer name"), _("Thicknes"), _("Optical material"), _("Layer type"), _("Solve optical\nproblem"), _("ID")])
		self.tab2.json_root_path="epitaxy"
		self.tab2.setColumnWidth(1, 125)
		self.tab2.setColumnWidth(2, 250)
		self.tab2.setColumnWidth(3, 120)
		self.tab2.setColumnWidth(5, 10)
		self.tab2.populate()
		self.tab2.new_row_clicked.connect(self.callback_new_row_clicked)
		self.tab2.changed.connect(self.emit_structure_changed)
		self.tab2.itemSelectionChanged.connect(self.layer_selection_changed)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)


		self.color_map=QColorMap(self)

		self.color_map.changed.connect(self.callback_random_colors)
		self.color_map.setEnabled(False)
		#self.colors.setCheckable(True)
		self.toolbar.addAction(self.color_map)

		self.main_vbox.addWidget(self.toolbar)

		self.main_vbox.addWidget(self.tab2)
		self.status_bar=QStatusBar()
		self.main_vbox.addWidget(self.status_bar)	
		self.setLayout(self.main_vbox)
		self.update_colors()

	def callback_tab_selection_changed(self):
		self.emit_change()

	def emit_change(self):
		self.update_colors()
		global_object_run("gl_force_redraw_hard")
		
	def emit_structure_changed(self,token):
		self.save_model()
		if token!="solve_optical_problem" and token!="solve_thermal_problem":  
			global_object_run("dos_update")
			global_object_run("pl_update")
			global_object_run("interface_update")
			global_object_run("mesh_update")
			global_object_run("optics_force_redraw")
			global_object_run("gl_force_redraw_hard")

	def callback_random_colors(self):
		lines=self.tab2.selectionModel().selectedRows()
		y=0
		segments=self.bin.get_token_value("epitaxy","segments")
		for l in lines:
			row=l.row()
			if row>=0 and row<segments:
				r,g,b=self.color_map.get_color(float(row)/float(segments))
				self.bin.set_token_value("epitaxy.segment"+str(row),"color_r",float(r)/255.0)
				self.bin.set_token_value("epitaxy.segment"+str(row),"color_g",float(g)/255.0)
				self.bin.set_token_value("epitaxy.segment"+str(row),"color_b",float(b)/255.0)
		self.bin.save()
		global_object_run("gl_force_redraw_hard")

	def callback_new_row_clicked(self,row):
		self.emit_structure_changed("all")

	def save_model(self):
		self.bin.lib.json_epitaxy_symc_to_mesh(ctypes.byref(json_tree_c()))
		self.bin.save()

	def layer_selection_changed(self):
		a=self.tab2.selectionModel().selectedRows()

		if len(a)>0:
			y=a[0].row()
			layer_id=self.bin.get_token_value("epitaxy.segment"+str(y),"id")
			layer_name=self.bin.get_token_value("epitaxy.segment"+str(y),"name")
			global_object_get("display_set_selected_obj")(layer_id)
			layer_start=self.bin.lib.json_epitaxy_get_layer_start(ctypes.byref(json_tree_c()),y)
			layer_stop=self.bin.lib.json_epitaxy_get_layer_stop(ctypes.byref(json_tree_c()),y)
			start_mul,start_units= distance_with_units(layer_start)
			stop_mul,stop_units= distance_with_units(layer_stop)
			self.status_bar.showMessage(layer_name+" "+_("start:")+" "+"{:.3f}".format(start_mul*layer_start)+start_units+" "+_("stop:")+" "+"{:.3f}".format(stop_mul*layer_stop)+" "+stop_units)

		self.color_map.blockSignals(True)
		if len(a)==0:
			self.color_map.setEnabled(False)
		else:
			self.color_map.setEnabled(True)
		self.color_map.blockSignals(False)

	def update_colors(self):
		error_found=False
		for y in range(self.tab2.rowCount()):
			path=str(self.tab2.get_value(y,2))
			full_path=os.path.join(sim_paths.get_materials_path(),path)
			if os.path.isfile(full_path)==False and os.path.isdir(full_path)==False:
				self.tab2.set_row_color( y, QColor('red'))
				error_found=True
			else:
				self.tab2.set_row_color( y, QColor('white'))


		if error_found==True:
			self.warning=_("Red=not found in materials DB")
			self.status_bar.showMessage(self.warning)

	def fixup_new_row(self,row):
		pass


