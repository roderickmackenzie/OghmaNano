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
#  The doping dialog.
#

import os
from icon_lib import icon_get

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidgetItem,QAbstractItemView
from PySide2.QtGui import QPainter,QIcon

#pyqtgraph
from pyqtgraph import PlotWidget, plot
from pyqtgraph.graphicsItems.ViewBox import axisCtrlTemplate_pyside2
from pyqtgraph.graphicsItems.PlotItem import plotConfigTemplate_pyside2
from pyqtgraph.imageview import ImageViewTemplate_pyside2
import pyqtgraph as pg

from open_save_dlg import save_as_image
from QWidgetSavePos import QWidgetSavePos
from cal_path import sim_paths

from epitaxy import epitaxy_get_epi
from error_dlg import error_dlg

#from file_watch import get_watch
from g_tab2 import g_tab2
from epitaxy import get_epi
from json_root import json_root
from help import QAction_help
import numpy as np

class doping_window(QWidgetSavePos):


	def update(self):
		self.build_mesh()
		self.draw_graph()


	def draw_graph(self):
		self.canvas.clear()

		plot0=self.canvas
		plot0.addLegend()
		plot0.setLogMode(False, True)
		plot0.setLabel('left', _("Charge denisty (m^{-3})"), color='k')
		plot0.setLabel('bottom','Position (nm)', color='k')
		plot0.getAxis('left').enableAutoSIPrefix(False)
		plot0.showGrid(x = True, y = True, alpha = 1.0)

		plot0.setRange(xRange=[min(self.x_pos),max(self.x_pos)])
		
		x_plot=[]
		for i in range(0,len(self.x_pos)):
			x_plot.append(self.x_pos[i]*1e9)

		#self.ax1.set_yscale('symlog')
		x = np.array(x_plot)
		if self.Na_enabled==True:
			pen = pg.mkPen((255, 0, 0), width=3)
			plot0.plot(x=self.x_pos_Na, y=self.doping_Na, pen=pen, name=_("Na"), symbol='o', symbolSize=8, symbolBrush =(255, 0, 0))

		if self.Nd_enabled==True:
			pen = pg.mkPen(( 0, 255, 0), width=3)
			plot0.plot(x=self.x_pos_Nd, y=self.doping_Nd, pen=pen, name=_("Nd"), symbol='o', symbolSize=8, symbolBrush =(0, 255, 0))

		if self.nion_enabled==True:
			pen = pg.mkPen(( 0, 0, 255), width=3)
			plot0.plot(x=self.x_pos_ions, y=self.ions, pen=pen, name=_("Ions"), symbol='o', symbolSize=8, symbolBrush =(0, 0, 255))


	def project(self,token0,token1):
		x_out=[]
		y_out=[]
		data=json_root()
		x,y =	data.electrical_solver.mesh.mesh_y.calculate_points()
		#print(x)
		device_start=data.epi.get_device_start(data)
		try:
			layer=self.epi.get_next_dos_layer(-1)

			for i in range(0,len(x)):
				if x[i]+device_start>self.epi.layers[layer].end:
					layer=layer+1

				Nad0=getattr(self.epi.layers[layer].shape_dos,token0)
				Nad1=getattr(self.epi.layers[layer].shape_dos,token1)

				dy=self.epi.layers[layer].dy
				y[i]=Nad0+(Nad1-Nad0)*(x[i]-self.epi.layers[layer].start+device_start)/dy
				if y[i]>0.0:
					x_out.append(x[i])
					y_out.append(y[i])
		except:
			pass
		return x_out,y_out

	def build_mesh(self):

		self.x_pos_Na,self.doping_Na=self.project("Na0","Na1")
		self.x_pos_Nd,self.doping_Nd=self.project("Nd0","Nd1")
		self.x_pos_ions,self.ions=self.project("ion_density","ion_density")
		self.x_pos,y =	json_root().electrical_solver.mesh.mesh_y.calculate_points()

		self.nion_enabled=False
		self.Nd_enabled=False
		self.Na_enabled=False

		if (len(self.x_pos_ions)>0):
			self.nion_enabled=True

		if (len(self.x_pos_Na)>0):
			self.Na_enabled=True

		if (len(self.x_pos_Nd)>0):
			self.Nd_enabled=True

		return True


	def __init__(self):
		QWidgetSavePos.__init__(self,"doping")
		self.setMinimumSize(1000, 600)
		self.setWindowIcon(icon_get("doping"))
		self.setWindowTitle2(_("Doping/Mobilie ion profile editor"))

		self.epi=get_epi()

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

		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		self.canvas = pg.PlotWidget()
		self.canvas.getPlotItem().setMouseEnabled(x=False, y=False)
		self.main_vbox.addWidget(self.canvas)

		#tab2
		self.tab2 = g_tab2()
		self.tab2.set_tokens(["name","shape_dos.Na0","shape_dos.Na1","shape_dos.Nd0","shape_dos.Nd1","shape_dos.ion_density","shape_dos.ion_mobility"])
		self.tab2.set_labels([_("Layer"),"Na0 (m^{-3})","Na1 (m^{-3})","Nd0 (m^{-3})","Nd1 (m^{-3})","Nion(+) (m^{-3})","Nion mu (m2 V^{-1}s^{-1})"])
		self.tab2.json_search_path="json_root().epi.layers"
		self.tab2.setColumnWidth(1, 120)
		self.tab2.setColumnWidth(2, 120)
		self.tab2.setColumnWidth(3, 120)
		self.tab2.setColumnWidth(4, 120)
		self.tab2.setColumnWidth(5, 140)
		self.tab2.setColumnWidth(6, 240)
		self.tab2.menu_disabled=True
		self.tab2.check_enabled_callback=self.check_enabled
		self.tab2.populate()
		self.tab2.changed.connect(self.callback_save)


		self.main_vbox.addWidget(self.tab2)
		self.update()

		self.setLayout(self.main_vbox)

	def callback_save(self):
		self.update()
		json_root().save()

	def check_enabled(self,s,token):
		if s.shape_dos.enabled==False:
			return False
		if token=="name":
			return False

		return True

