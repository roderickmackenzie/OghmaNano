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

## @package fxexperiment_mesh_tab
#  fx domain mesh editor
#

from util import fx_with_units
from icon_lib import icon_get

import i18n
_ = i18n.language.gettext

import pyqtgraph as pg

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget
from PySide2.QtGui import QPainter,QIcon

#windows
from open_save_dlg import save_as_jpg

from cal_path import sim_paths
from g_tab2 import g_tab2

import numpy as np
from json_fx_domain import json_fx_domain_mesh_segment
from json_root import json_root

class fxexperiment_mesh_tab(QWidget):

	def save_data(self):
		json_root().save()
		
	def update(self):
		self.build_mesh()
		self.draw_graph()

	def draw_graph(self):
		if len(self.fx)==0:
			return

		my_max=self.fx[0][0]
		my_min=self.fx[0][0]

		for i in range(0,len(self.fx)):
			for ii in range(0,len(self.fx[i])):
				if self.fx[i][ii]>my_max:
					my_max=self.fx[i][ii]

				if self.fx[i][ii]<my_min:
					my_min=self.fx[i][ii]
	
		mul=1.0
		unit="Hz"

		fx=[]
		mag=[]
		for i in range(0,len(self.fx)):
			local_fx=[]
			for ii in range(0,len(self.fx[i])):
				local_fx.append(self.fx[i][ii]*mul)
				mag.append(1)
			fx.extend(local_fx)

		self.plot.clear()
		self.plot.getAxis('bottom').enableAutoSIPrefix(False)
		self.plot.getPlotItem().hideAxis('left')
		self.plot.getPlotItem().setMouseEnabled(x=False, y=False)		
		scatter = pg.ScatterPlotItem()

		#here
		pi = self.plot.getPlotItem()
		ai = pi.getAxis("bottom")
		ai.setLogMode(True)

		#spots = []
		brush=[]
		for i in range(0,len(fx)):
			#spot_dic = {'pos': (fx[i], 1), 'size': 10, 'brush': pg.intColor(i, len(fx)), 'pen': None}
			#spots.append(spot_dic)
			brush.append(pg.intColor(i, len(fx)))

		#scatter.addPoints(spots)
		my_plot = pi.plot(fx,mag, size=10, pen=None, symbolBrush=brush)
		#my_plot.addItem(scatter)
		my_plot.setLogMode(True, False)
		#self.plot.addItem(scatter)
		self.plot.setLogMode(True, False)
		self.plot.setLabel('bottom', _("Frequency")+" ("+unit+")", color='k')



	def build_mesh(self):
		self.mag=[]
		self.fx=[]
		data=json_root().sims.fx_domain.find_object_by_id(self.uid)

		for mesh_item in data.mesh.segments:
			local_mag=[]
			local_fx=[]
			start=mesh_item.start
			fx=start
			stop=mesh_item.stop
			max_points=mesh_item.points
			mul=mesh_item.mul
			pos=0
			if stop!=0.0 and max_points!=0.0 and mul!=0.0:
				if max_points==1:
					local_fx.append(fx)
					local_mag.append(1.0)
				else:
					fx_start=fx
					while(fx<stop):
						local_fx.append(fx)
						local_mag.append(1.0)
						if mul==1.0:
							fx=fx+(stop-fx_start)/max_points
						else:
							fx=fx*mul
						pos=pos+1
						if pos>max_points:
							break

			self.mag.append(local_mag)
			self.fx.append(local_fx)
			local_mag=[]
			local_fx=[]



	def redraw_and_save(self):
		self.update()
		self.save_data()

	def on_cell_edited(self):
		self.redraw_and_save()

	def __init__(self,uid):
		QWidget.__init__(self)
		self.uid=uid
		self.ax1=None

		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		self.plot = pg.PlotWidget()
		self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		self.main_vbox = QHBoxLayout()

		self.main_vbox.addWidget(self.plot)


		#toolbar 2

		toolbar2=QToolBar()
		toolbar2.setIconSize(QSize(32, 32))

		tab_holder=QWidget()
		tab_vbox_layout= QVBoxLayout()
		tab_holder.setLayout(tab_vbox_layout)
		self.tab = g_tab2(toolbar=toolbar2)

		self.tab.set_tokens(["start","stop","points","mul"])
		self.tab.set_labels([_("Frequency start"),_("Frequency stop"), _("Max points"), _("Multiply")])

		self.tab.setColumnWidth(0, 200)
		self.tab.setColumnWidth(1, 200)

		data=json_root().sims.fx_domain.find_object_by_id(self.uid)
		index=json_root().sims.fx_domain.segments.index(data)
		self.tab.json_search_path="json_root().sims.fx_domain.segments["+str(index)+"].mesh.segments"

		self.tab.populate()

		self.tab.new_row_clicked.connect(self.callback_new_row_clicked)
		self.tab.changed.connect(self.on_cell_edited)

		self.tab.setMinimumSize(self.width(), 120)

		tab_vbox_layout.addWidget(toolbar2)

		self.build_mesh()
		self.draw_graph()

		tab_vbox_layout.addWidget(self.tab)
		self.main_vbox.addWidget(tab_holder)

		self.setLayout(self.main_vbox)

	def callback_new_row_clicked(self,row):
		obj=json_fx_domain_mesh_segment()
		json_root().sims.fx_domain.find_object_by_id(self.uid).mesh.segments.insert(row,obj)
		self.tab.insert_row(obj,row)


