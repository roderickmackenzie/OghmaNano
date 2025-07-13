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

## @package tab_mesh_editor
#  A tab to edit the electrical mesh.
#

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QToolBar, QVBoxLayout, QGroupBox, QAction
from gQtCore import gSignal

from util import distance_with_units
from icon_lib import icon_get

from g_tab2_bin import g_tab2_bin

from dat_file import dat_file
from mesh_math import mesh_math
from json_c import json_tree_c
from graph import graph_widget
from color_map import color_map

class tab_mesh_editor(QGroupBox):

	changed = gSignal()

	def __init__(self,json_path,no_user_edit=False,show_auto=False,one_point_per_layer=False):
		QGroupBox.__init__(self)
		self.bin=json_tree_c()
		self.json_path=json_path
		self.mesh_math=mesh_math(json_path)
		self.show_auto=show_auto
		self.one_point_per_layer=one_point_per_layer
		self.no_user_edit=no_user_edit
		self.setMinimumWidth(250)
		self.cm=color_map()
		self.cm.find_map("Rainbow")
		self.xyz=""

		if self.mesh_math.direction=="l":
			self.setTitle(_("Wavelength"))
		elif self.mesh_math.direction=="t":
			self.setTitle(_("Temperature"))
		else:
			self.setTitle(self.mesh_math.direction)

		self.setStyleSheet("QGroupBox {  border: 1px solid gray;}")
		vbox=QVBoxLayout()
		self.setLayout(vbox)

		self.toolbar=QToolBar()
		self.toolbar.setIconSize(QSize(32, 32))

		vbox.addWidget(self.toolbar)

		self.tab = g_tab2_bin(toolbar=self.toolbar)

		self.tb_mesh_auto = QAction(icon_get("mesh_auto"), _("Mesh Auto"), self)
		self.tb_mesh_auto.setCheckable(True)
		auto=self.bin.get_token_value(self.json_path,"auto")
		self.tb_mesh_auto.setChecked(auto)
		self.tb_mesh_auto.triggered.connect(self.callback_mesh_auto)

		if self.show_auto==True:
			self.toolbar.addAction(self.tb_mesh_auto)
		
		if self.mesh_math.direction=="l":
			self.tab.set_override_widgets(["edit_with_units","edit_with_units","",""])
			self.tab.set_tokens(["start","stop","mul","points"])
			self.tab.set_labels([_("Start"), _("Stop"), _("Step multiply"), _("points")])
			self.tab.setColumnWidth(0, 150)
			self.tab.setColumnWidth(1, 150)
		elif self.mesh_math.direction=="t":
			self.tab.set_tokens(["start","stop","mul","points"])
			self.tab.set_labels([_("Start"), _("Stop"), _("Step multiply"), _("points")])
		else:
			self.tab.set_tokens(["len","points","mul","left_right"])
			self.tab.set_labels([_("Thicknes"), _("Mesh points"), _("Step multiply"), _("Left/Right")])
			self.tab.setColumnWidth(0, 150)

		self.tab.json_root_path=self.json_path

		self.tab.populate()
		self.tab.changed.connect(self.emit_structure_changed)
		vbox.addWidget(self.tab)

		self.plot2=graph_widget()
		self.plot2.graph.cm_default=self.cm.map
		self.plot2.graph.axis_y.hidden=True;
		self.plot2.graph.points=True;
		self.plot2.graph.lines=False;
		self.plot2.setMaximumHeight(200)
		self.plot2.setMinimumHeight(200)
		vbox.addWidget(self.plot2)
		self.update()
		self.redraw()

	def redraw(self):
		self.x=[]
		self.mag=[]

		d=dat_file()
		x_ret,self.mag=self.mesh_math.calculate_points(one_point_per_layer=self.one_point_per_layer)
		self.mesh_math.gen_dat_file(d)
		self.plot2.load([d])
		self.plot2.graph.info[0].color_map_within_line=True
		#d.dump_info()
		d.free()
		self.plot2.update()
		#mul,unit=distance_with_units(tot)
		#if self.mesh_math.direction=="t":
		#	unit="Kelvin"
		#	mul=1.0

		#if self.mesh_math.direction=="l":
		#	self.plot.setLabel('bottom', _("Wavelength"), units=str(unit), color='k')
		#elif self.mesh_math.direction=="t":
		#	self.plot.setLabel('bottom', _("Temperature"), units=str(unit), color='k')
		#else:
		#	self.plot.setLabel('bottom', _("Thickness"), units=str(unit), color='k')


	def update(self):
		if self.show_auto==True:
			auto=self.bin.get_token_value(self.json_path,"auto")
			if auto==True:
				self.tab.setEnabled(False)
				self.plot2.setHidden(True)
			else:
				self.tab.setEnabled(True)
				self.plot2.setHidden(False)

		if self.no_user_edit==True:
			self.tab.tb_add.setEnabled(False)
			self.tab.tb_remove.setEnabled(False)
			self.tab.tb_up.setEnabled(False)
			self.tab.tb_down.setEnabled(False)
			self.tab.setEnabled(False)


	def callback_mesh_auto(self):
		self.bin.set_token_value(self.json_path,"auto",self.tb_mesh_auto.isChecked())
		self.update()
		self.bin.save()

	def emit_structure_changed(self):
		self.redraw()
		self.changed.emit()
		self.bin.save()
