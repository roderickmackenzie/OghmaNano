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

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget
from PySide2.QtGui import QPainter,QIcon

#windows
from open_save_dlg import save_as_jpg
from cal_path import sim_paths
from g_tab2_bin import g_tab2_bin
from json_c import json_tree_c
import ctypes
from bytes2str import str2bytes
from graph import graph_widget
from dat_file import dat_file
from color_map import color_map

class fxexperiment_mesh_tab(QWidget):

	def __init__(self,json_search_path,uid):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.cm=color_map()
		self.cm.find_map("Rainbow")

		self.json_search_path=json_search_path
		self.uid=uid

		self.data=dat_file()

		self.plot2=graph_widget()
		self.plot2.graph.axis_y.hidden=True;
		self.plot2.graph.cm_default=self.cm.map
		self.plot2.graph.points=True;
		self.plot2.graph.lines=False;
		self.plot2.setMaximumHeight(200)
		self.plot2.setMinimumHeight(200)
		self.plot2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.plot2.setMinimumSize(600, 250)

		self.main_vbox = QVBoxLayout()


		#toolbar 2

		toolbar2=QToolBar()
		toolbar2.setIconSize(QSize(32, 32))

		tab_holder=QWidget()
		tab_vbox_layout= QVBoxLayout()
		tab_holder.setLayout(tab_vbox_layout)
		self.tab = g_tab2_bin(toolbar=toolbar2)

		self.tab.set_tokens(["start","stop","points","mul"])
		self.tab.set_labels([_("Frequency start"),_("Frequency stop"), _("Max points"), _("Multiply")])

		self.tab.setColumnWidth(0, 200)
		self.tab.setColumnWidth(1, 200)

		json_path=self.refind_json_path()
		self.tab.json_root_path=json_path+".mesh"

		self.tab.populate()

		self.tab.changed.connect(self.on_cell_edited)

		self.tab.setMinimumSize(self.width(), 120)

		tab_vbox_layout.addWidget(toolbar2)

		self.build_mesh()
		self.draw_graph()

		tab_vbox_layout.addWidget(self.tab)
		self.main_vbox.addWidget(self.plot2)
		self.main_vbox.addWidget(tab_holder)

		self.setLayout(self.main_vbox)

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid("sims.fx_domain",self.uid)
		return ret

	def save_data(self):
		self.bin.save()
		
	def update(self):
		self.build_mesh()
		self.draw_graph()

	def draw_graph(self):

		if self.fx==[] or self.fx==[[]]:
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

		fx=[]
		mag=[]
		for i in range(0,len(self.fx)):
			local_fx=[]
			for ii in range(0,len(self.fx[i])):
				local_fx.append(self.fx[i][ii]*mul)
				mag.append(1)
			fx.extend(local_fx)

		self.data.x_len=1
		self.data.y_len=len(fx)
		self.data.z_len=1
		self.data.cols=b"yd"
		self.data.type=b"xy"
		self.data.data_label=b""
		self.data.data_units=b""
		self.data.y_label=b"Frequency"
		self.data.y_units=b"Hz"
		self.data.y_mul=1e9
		self.plot2.graph.cm_default=self.cm.map
		self.plot2.graph.axis_x.log_scale=True
		self.plot2.graph.lib.dat_file_malloc_py_data(ctypes.byref(self.data))
		self.plot2.graph.show_key=True

		for i in range(0,self.data.y_len):
			self.data.y_scaleC[i]=fx[i]
			self.data.py_data[0][0][i]=1.0

		self.plot2.load([self.data])
		self.plot2.graph.info[0].color_map_within_line=True
		self.plot2.update()


	def __del__(self):
		self.data.free()

	def build_mesh(self):
		self.mag=[]
		self.fx=[]
		json_path=self.refind_json_path()
		segments=self.bin.get_token_value(json_path+".mesh","segments")

		for seg in range(0,segments):
			local_mag=[]
			local_fx=[]
			start=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"start")
			fx=start
			stop=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"stop")
			max_points=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"points")
			mul=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"mul")
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
		self.plot2.update()
		self.redraw_and_save()


