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

from json_root import json_root
from json_mesh import json_mesh_segment
from json_mesh import json_mesh_lambda
from json_mesh import json_mesh_thermal

from g_tab2 import g_tab2

from dat_file import dat_file
import pyqtgraph as pg

class tab_mesh_editor(QGroupBox):

	changed = gSignal()

	def redraw(self):
		self.x=[]
		self.mag=[]
		data=eval(self.json_path)
		
		x_ret,self.mag=data.calculate_points(root_data=json_root())
		tot=0
		if len(x_ret)>1:
			tot=x_ret[len(x_ret)-1]

		mul,unit=distance_with_units(tot)
		if data.direction=="t":
			unit="Kelvin"
			mul=1.0

		self.plot.clear()
		self.plot.getPlotItem().hideAxis('left')
		self.plot.getPlotItem().setMouseEnabled(x=False, y=False)
		scatter = pg.ScatterPlotItem()

		spots = []
		for i in range(0,len(x_ret)):
			spot_dic = {'pos': (x_ret[i]*mul, 1), 'size': 10, 'brush': pg.intColor(i, len(x_ret)), 'pen': None}
			spots.append(spot_dic)

		scatter.addPoints(spots)

		self.plot.addItem(scatter)
		if data.direction=="l":
			self.plot.setLabel('bottom', _("Wavelength"), units=str(unit), color='k')
		elif data.direction=="t":
			self.plot.setLabel('bottom', _("Temperature"), units=str(unit), color='k')
		else:
			self.plot.setLabel('bottom', _("Thickness"), units=str(unit), color='k')


	def get_json(self):
		return eval(self.json_path)

	def __init__(self,json_path,no_user_edit=False,show_auto=False):
		self.json_path=json_path
		self.show_auto=show_auto
		self.no_user_edit=no_user_edit
		data=self.get_json()

		QGroupBox.__init__(self)
		self.xyz=""

		if data.direction=="l":
			self.setTitle(_("Wavelength"))
		elif data.direction=="t":
			self.setTitle(_("Temperature"))
		else:
			self.setTitle(data.direction)

		self.setStyleSheet("QGroupBox {  border: 1px solid gray;}")
		vbox=QVBoxLayout()
		self.setLayout(vbox)

		self.toolbar=QToolBar()
		self.toolbar.setIconSize(QSize(32, 32))

		vbox.addWidget(self.toolbar)

		self.tab = g_tab2(toolbar=self.toolbar)

		self.tb_mesh_auto = QAction(icon_get("mesh_auto"), _("Mesh Auto"), self)
		self.tb_mesh_auto.setCheckable(True)
		self.tb_mesh_auto.setChecked(data.auto)
		self.tb_mesh_auto.triggered.connect(self.callback_mesh_auto)

		if self.show_auto==True:
			self.toolbar.addAction(self.tb_mesh_auto)
		
		if data.direction=="l":
			self.tab.set_tokens(["start","stop","mul","points"])
			self.tab.set_labels([_("Start"), _("Stop"), _("Step multiply"), _("points")])
		elif data.direction=="t":
			self.tab.set_tokens(["start","stop","mul","points"])
			self.tab.set_labels([_("Start"), _("Stop"), _("Step multiply"), _("points")])
		else:
			self.tab.set_tokens(["len","points","mul","left_right"])
			self.tab.set_labels([_("Thicknes"), _("Mesh points"), _("Step multiply"), _("Left/Right")])

		self.tab.json_search_path=self.json_path+".segments"

		self.tab.populate()
		self.tab.changed.connect(self.emit_structure_changed)
		vbox.addWidget(self.tab)
		if data.direction=="l":
			self.tab.base_obj=json_mesh_lambda()
		elif data.direction=="t":
			self.tab.base_obj=json_mesh_thermal()
		else:
			self.tab.base_obj=json_mesh_segment()

		pg.setConfigOptions(antialias = True)

		# creating a plot window
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		self.plot = pg.PlotWidget()
		self.plot.setMaximumHeight(200)
		vbox.addWidget(self.plot)
		self.update()
		self.redraw()

	def update(self):
		data=self.get_json()
		if self.show_auto==True:
			if data.auto==True:
				self.tab.setEnabled(False)
				self.plot.setHidden(True)
			else:
				self.tab.setEnabled(True)
				self.plot.setHidden(False)

		if self.no_user_edit==True:
			self.tab.tb_add.setEnabled(False)
			self.tab.tb_remove.setEnabled(False)
			self.tab.tb_up.setEnabled(False)
			self.tab.tb_down.setEnabled(False)
			self.tab.setEnabled(False)


	def callback_mesh_auto(self):
		data=self.get_json()
		data.auto=self.tb_mesh_auto.isChecked()
		self.update()
		json_root().save()

	def emit_structure_changed(self):
		self.redraw()
		self.changed.emit()
		json_root().save()
