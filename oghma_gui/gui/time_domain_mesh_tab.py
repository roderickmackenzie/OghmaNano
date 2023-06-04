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

## @package time_domain_mesh_tab
#  A mesh editor for the time domain mesh.
#


import os
from dlg_get_text2 import dlg_get_text2
from util import time_with_units
from cal_path import get_icon_path


#pyqtgraph
from pyqtgraph import PlotWidget, plot
from pyqtgraph.graphicsItems.ViewBox import axisCtrlTemplate_pyside2
from pyqtgraph.graphicsItems.PlotItem import plotConfigTemplate_pyside2
from pyqtgraph.imageview import ImageViewTemplate_pyside2
import pyqtgraph as pg

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView
from PySide2.QtGui import QPainter,QIcon

#windows
from open_save_dlg import save_as_image
from cal_path import sim_paths
from icon_lib import icon_get
from g_tab2 import g_tab2
from json_root import json_root
from json_time_domain import json_time_domain_mesh_segment
import i18n
_ = i18n.language.gettext
from math import exp
from math import pow

class tab_time_mesh(QWidget):

	def save_data(self):
		json_root().save()



	def callback_laser(self):
		data=json_root().sims.time_domain.find_object_by_id(self.uid)
		new_time=dlg_get_text2( _("Enter the time at which the laser pulse will fire (-1) to turn it off"), str(data.config.fs_laser_time),"laser.png")
		new_time=new_time.ret

		if new_time!=None:
			data.config.fs_laser_time=float(new_time)
			self.build_mesh()
			self.draw_graph()
			json_root().save()

	def update(self):
		self.build_mesh()
		self.draw_graph()

	def on_cell_edited(self):
		self.save_data()
		self.build_mesh()
		self.draw_graph()

	def gaussian(self,start, stop, mu, sig,x_mul=1.0):
		x=[]					#avoiding numpy
		y=[]
		pos=start
		dx=(stop-start)/20.0
		while(pos<stop):
			x.append(pos*x_mul)
			y.append(exp(-pow(pos - mu, 2.) / (2 * pow(sig, 2.))))
			pos=pos+dx
		return x,y

	def draw_graph(self):
		fs_laser_time=json_root().sims.time_domain.find_object_by_id(self.uid).config.fs_laser_time
		if (len(self.time)>0):
			mul,unit=time_with_units(float(self.time[len(self.time)-1]-self.time[0]))
		else:
			mul=1.0
			unit="s"

		time=[]
		for i in range(0,len(self.time)):
			time.append(self.time[i]*mul)

		self.canvas.clear()

		pen = pg.mkPen((255, 0, 0), width=3)

		plot0=self.canvas.addPlot(row=0, col=0)
		plot0.addLegend()
		plot0.plot(x=time, y=self.voltage, pen=pen, name=_("Voltage"), symbol='o', symbolSize=8, symbolBrush =(255, 0, 0))
		plot0.setLabel('left', _("Voltage")+" (Volts)", color='k')
		plot0.setLabel('bottom', _("Time") +" ("+unit+")", color='k')
		plot0.showGrid(x = True, y = True, alpha = 1.0)
		#plot0.hideAxis('bottom')

		pen = pg.mkPen((0, 255, 0), width=3)
		plot1=self.canvas.addPlot( row=1, col=0)
		plot1.addLegend()
		plot1.plot(x=time, y=self.sun, pen=pen,  name=_("Sun"), symbol='o', symbolSize=8, symbolBrush =(0, 255, 0))
		plot1.setLabel('left', _("Suns")+" (Suns)", color='k')
		plot1.setLabel('bottom', _("Time")+" ("+unit+")", color='k')
		plot0.setXLink(plot1)
		plot1.showGrid(x = True, y = True, alpha = 1.0)

		pen = pg.mkPen((0, 0, 255), width=3)
		plot1.plot(time,self.laser, pen=pen, symbol='o', symbolSize=8, name=_("Laser"), symbolBrush =(0, 0, 255))

		if fs_laser_time!=-1:
			if len(self.time)>2:
				dt=(self.time[len(time)-1]-self.time[0])/100
				start=fs_laser_time-dt*5
				stop=fs_laser_time+dt*5
				x,y=self.gaussian(start,stop,fs_laser_time,dt,x_mul=mul)
				pen = pg.mkPen((0, 255, 0), width=3)
				plot1.plot(x,y, pen=pen, name=_("fs Laser"))

	def build_mesh(self):

		self.laser=[]
		self.sun=[]
		self.voltage=[]
		self.time=[]
		self.fs_laser=[]
		data=json_root().sims.time_domain.find_object_by_id(self.uid)
		mesh=data.mesh
		pos=data.config.start_time
		fired=False

		laser_pulse_width=0.0


		float(json_root().optical.light.Psun)

		voltage_bias=data.config.pulse_bias
		fs_laser_time=data.config.fs_laser_time

		for seg in mesh.segments:
			length=seg.len
			end_time=pos+length

			dt=seg.dt
			if dt<=0.0:
				dt=length/10

			voltage_start=seg.voltage_start
			voltage_stop=seg.voltage_stop

			laser_start=seg.laser_start
			laser_stop=seg.laser_stop

			sun_start=seg.sun_start
			sun_stop=seg.sun_stop

			mul=seg.mul
			if mul<=0:
				mul=1.0

			#print("VOLTAGE=",line[SEG_VOLTAGE],end_time,pos)

			if (length/dt)>100:
				dt=length/100

			voltage=voltage_start
			laser=laser_start
			sun=sun_start
			while(pos<end_time):
				dv=(voltage_stop-voltage_start)*(dt/length)
				dlaser=(laser_stop-laser_start)*(dt/length)
				dsun=(sun_stop-sun_start)*(dt/length)
				self.time.append(pos)
				self.laser.append(laser)
				self.sun.append(sun)
				self.voltage.append(voltage+voltage_bias)
				self.fs_laser.append(0.0)
				pos=pos+dt
				voltage=voltage+dv
				laser=laser+dlaser
				sun=sun+dsun

				if fired==False:
					if pos>fs_laser_time and fs_laser_time!=-1:
						fired=True
						self.fs_laser[len(self.fs_laser)-1]=laser_pulse_width/dt

				dt=dt*mul


	def callback_start_time(self):
		data=json_root().sims.time_domain.find_object_by_id(self.uid)
		new_time=dlg_get_text2( _("Enter the start time of the simulation"), str(data.config.start_time),"start.png")
		new_time=new_time.ret

		if new_time!=None:
			data.config.start_time=float(new_time)
			self.build_mesh()
			self.draw_graph()
			json_root().save()


	def __init__(self,uid):
		self.uid=uid
		QWidget.__init__(self)
		self.main_vbox = QVBoxLayout()
		self.time=[]
		self.voltage=[]
		self.sun=[]
		self.laser=[]

		self.edit_list=[]
		self.line_number=[]
		self.list=[]

		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		self.canvas = pg.GraphicsLayoutWidget()#pg.PlotWidget()

		self.show_key=True

		self.main_vbox.addWidget(self.canvas)

		#toolbar 2

		toolbar2=QToolBar()
		toolbar2.setIconSize(QSize(32, 32))

		self.main_vbox.addWidget(toolbar2)
	
		self.tab = g_tab2(toolbar=toolbar2)
		self.tab.set_tokens(["len","dt","voltage_start","voltage_stop","mul","sun_start","sun_stop","laser_start","laser_stop"])
		self.tab.set_labels([_("Length"),_("dt"), _("Start Voltage"), _("Stop Voltage"), _("step multiplyer"), _("Sun start"), _("Sun stop"),_("Laser start"),_("Laser stop")])

		self.tab.setMinimumSize(self.width(), 120)

		data=json_root().sims.time_domain.find_object_by_id(self.uid)
		index=json_root().sims.time_domain.segments.index(data)
		self.tab.json_search_path="json_root().sims.time_domain.segments["+str(index)+"].mesh.segments"
		self.tab.base_obj=json_time_domain_mesh_segment()

		self.tab.populate()
		
		self.tab.changed.connect(self.on_cell_edited)

		self.build_mesh()
		self.draw_graph()

		self.main_vbox.addWidget(self.tab)


		self.setLayout(self.main_vbox)




