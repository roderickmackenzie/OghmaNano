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

from icon_lib import icon_get
from global_objects import global_object_get
from g_tab2 import g_tab2
from PySide2.QtWidgets import QVBoxLayout ,QToolBar
from global_objects import global_object_run
from global_objects import global_object_get
from QWidgetSavePos import QWidgetSavePos
from epitaxy import get_epi
from json_root import json_root
from epitaxy_class import epi_layer

import i18n
_ = i18n.language.gettext

class layer_widget(QWidgetSavePos):

	def callback_tab_selection_changed(self):
		self.emit_change()

	def emit_change(self):
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


	def __init__(self):
		QWidgetSavePos.__init__(self,"layer_widget")

		self.setWindowTitle2(_("Layer editor"))
		self.setWindowIcon(icon_get("layers"))
		self.resize(800,500)

		self.main_vbox=QVBoxLayout()

		self.toolbar=QToolBar()

		self.tab2 = g_tab2(toolbar=self.toolbar)
		self.tab2.set_tokens(["name","dy","optical_material","layer_type","solve_optical_problem","solve_thermal_problem","id"])
		self.tab2.set_labels([_("Layer name"), _("Thicknes")+" (m)", _("Optical material"), _("Layer type"), _("Solve optical\nproblem"), _("Solve thermal\nproblem"), _("ID")])
		self.tab2.json_search_path="json_root().epitaxy.layers"
		self.tab2.setColumnWidth(2, 250)
		self.tab2.setColumnWidth(6, 10)
		self.tab2.populate()
		self.tab2.new_row_clicked.connect(self.callback_new_row_clicked)
		self.tab2.changed.connect(self.emit_structure_changed)
		self.tab2.base_obj=epi_layer()
		self.tab2.itemSelectionChanged.connect(self.layer_selection_changed)

		self.main_vbox.addWidget(self.toolbar)

		self.main_vbox.addWidget(self.tab2)
		self.setLayout(self.main_vbox)

	def callback_new_row_clicked(self,row):
		#epi=get_epi()
		#obj=epi.add_new_layer(pos=row)
		#self.tab2.insert_row(obj,row)
		self.emit_structure_changed("all")

	def save_model(self):
		epi=get_epi()
		data=json_root()
		epi.symc_to_mesh(data.electrical_solver.mesh.mesh_y)
		data.save()

	def layer_selection_changed(self):
		a=self.tab2.selectionModel().selectedRows()

		if len(a)>0:
			y=a[0].row()
			epi=get_epi()
			global_object_get("display_set_selected_obj")(epi.layers[y].id)



