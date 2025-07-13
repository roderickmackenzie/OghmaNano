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

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView
from PySide2.QtGui import QPainter,QIcon

#windows
from open_save_dlg import save_as_image
from cal_path import sim_paths
from icon_lib import icon_get
from g_tab2_bin import g_tab2_bin
import i18n
_ = i18n.language.gettext
from math import exp
from math import pow
from json_c import json_tree_c

import ctypes
from bytes2str import str2bytes
from graph import graph_widget
from dat_file import dat_file

class tab_time_mesh(QWidget):

	def __init__(self,uid):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.uid=uid
		self.main_vbox = QVBoxLayout()
		self.time=[]
		self.voltage=[]
		self.sun=[]
		self.laser=[]

		self.edit_list=[]
		self.line_number=[]
		self.list=[]

		self.data_voltage=dat_file()
		self.data_sun=dat_file()
		self.data_laser=dat_file()

		self.canvas_voltage = graph_widget()
		self.canvas_voltage.graph.axis_y.log_scale_auto=False
		self.canvas_voltage.graph.axis_y.log_scale=False
		self.canvas_voltage.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.canvas_voltage.setMinimumSize(400, 150)
		self.canvas_voltage.graph.points=True
		self.main_vbox.addWidget(self.canvas_voltage)

		self.canvas_sun = graph_widget()
		self.canvas_sun.graph.axis_y.log_scale_auto=False
		self.canvas_sun.graph.axis_y.log_scale=False
		self.canvas_sun.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.canvas_sun.setMinimumSize(400, 150)
		self.canvas_sun.graph.points=True
		self.main_vbox.addWidget(self.canvas_sun)

		#toolbar 2

		toolbar2=QToolBar()
		toolbar2.setIconSize(QSize(32, 32))

		self.main_vbox.addWidget(toolbar2)
	
		self.tab = g_tab2_bin(toolbar=toolbar2)
		self.tab.set_tokens(["len","dt","voltage_start","voltage_stop","mul","sun_start","sun_stop","laser_start","laser_stop"])
		self.tab.set_labels([_("Length"),_("dt"), _("Start Voltage"), _("Stop Voltage"), _("step multiplyer"), _("Sun start"), _("Sun stop"),_("Laser start"),_("Laser stop")])

		self.tab.setMinimumSize(self.width(), 120)
		
		json_path=self.refind_json_path()

		self.tab.json_root_path=json_path+".mesh"

		self.tab.populate()
		
		self.tab.changed.connect(self.on_cell_edited)

		self.build_mesh()
		self.draw_graph()

		self.main_vbox.addWidget(self.tab)

		self.setLayout(self.main_vbox)

	def __del__(self):
		self.canvas_sun.graph.lib.dat_file_free(ctypes.byref(self.data_voltage))
		self.canvas_sun.graph.lib.dat_file_free(ctypes.byref(self.data_sun))
		self.canvas_sun.graph.lib.dat_file_free(ctypes.byref(self.data_laser))

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid("sims.time_domain",self.uid)
		return ret

	def save_data(self):
		self.bin.save()

	def callback_laser(self):
		json_path=self.refind_json_path()
		fs_laser_time=self.bin.get_token_value(json_path+".config","fs_laser_time")
		new_time=dlg_get_text2( _("Enter the time at which the laser pulse will fire (-1) to turn it off"), str(fs_laser_time),"laser.png")
		new_time=new_time.ret

		if new_time!=None:
			self.bin.set_token_value(json_path+".config","fs_laser_time",float(new_time))
			self.build_mesh()
			self.draw_graph()
			self.bin.save()

	def update(self):
		self.build_mesh()
		self.draw_graph()

	def on_cell_edited(self):
		self.save_data()
		self.build_mesh()
		self.draw_graph()

	def gaussian(self,start, stop, mu, sig,x_mul=1.0):
		x=[]
		y=[]
		pos=start
		dx=(stop-start)/20.0
		while(pos<stop):
			x.append(pos*x_mul)
			y.append(exp(-pow(pos - mu, 2.) / (2 * pow(sig, 2.))))
			pos=pos+dx
		return x,y

	def draw_graph(self):
		json_path=self.refind_json_path()
		fs_laser_time=self.bin.get_token_value(json_path+".config","fs_laser_time")

		if (len(self.time)>0):
			mul,unit=time_with_units(float(self.time[len(self.time)-1]-self.time[0]))
		else:
			mul=1.0
			unit="s"

		self.data_sun.x_len=1
		self.data_sun.y_len=len(self.time)
		self.data_sun.z_len=1
		self.data_sun.cols=b"yd"
		self.data_sun.type=b"xy"
		self.data_sun.data_label=b"Light"
		self.data_sun.data_units=b"Suns"
		self.data_sun.y_label=b"Time"
		self.data_sun.y_units=unit.encode('utf-8')
		self.data_sun.y_mul=mul
		self.canvas_sun.graph.lib.dat_file_malloc_py_data(ctypes.byref(self.data_sun))
		self.canvas_sun.graph.show_key=True

		self.data_voltage.x_len=1
		self.data_voltage.y_len=len(self.time)
		self.data_voltage.z_len=1
		self.data_voltage.cols=b"yd"
		self.data_voltage.type=b"xy"
		self.data_voltage.data_label=b"Voltage"
		self.data_voltage.data_units=b"V"
		self.data_voltage.y_label=b"Time"
		self.data_voltage.y_units=unit.encode('utf-8')
		self.data_voltage.y_mul=mul
		self.canvas_sun.graph.lib.dat_file_malloc_py_data(ctypes.byref(self.data_voltage))
		self.canvas_voltage.graph.show_key=True


		self.data_laser.x_len=1
		self.data_laser.y_len=len(self.time)
		self.data_laser.z_len=1
		self.data_laser.cols=b"yd"
		self.data_laser.type=b"xy"
		self.data_laser.data_label=b"Laser"
		self.data_laser.data_units=b"au"
		self.data_laser.y_label=b"Time"
		self.data_laser.y_units=unit.encode('utf-8')
		self.data_laser.y_mul=mul
		self.canvas_sun.graph.lib.dat_file_malloc_py_data(ctypes.byref(self.data_laser))
		self.canvas_voltage.graph.show_key=True


		for i in range(0,self.data_sun.y_len):
			self.data_sun.y_scaleC[i]=self.time[i]
			self.data_sun.py_data[0][0][i]=self.sun[i]

			self.data_voltage.y_scaleC[i]=self.time[i]
			self.data_voltage.py_data[0][0][i]=self.voltage[i]

			self.data_laser.y_scaleC[i]=self.time[i]
			self.data_laser.py_data[0][0][i]=self.laser[i]

		self.canvas_sun.load([self.data_sun,self.data_laser],[0,1])
		self.canvas_sun.update()

		self.canvas_voltage.load([self.data_voltage])
		self.canvas_voltage.update()

		#if fs_laser_time!=-1:
		#	if len(self.time)>2:
		#		dt=(self.time[len(time)-1]-self.time[0])/100
		#		start=fs_laser_time-dt*5
		#		stop=fs_laser_time+dt*5
		#		x,y=self.gaussian(start,stop,fs_laser_time,dt,x_mul=mul)
		#		pen = pg.mkPen((0, 255, 0), width=3)
		#		plot1.plot(x,y, pen=pen, name=_("fs Laser"))

	def build_mesh(self):

		self.laser=[]
		self.sun=[]
		self.voltage=[]
		self.time=[]
		self.fs_laser=[]
		json_path=self.refind_json_path()

		pos=fs_laser_time=self.bin.get_token_value(json_path+".config","start_time")
		fired=False

		laser_pulse_width=0.0

		voltage_bias=self.bin.get_token_value(json_path+".config","pulse_bias")
		fs_laser_time=self.bin.get_token_value(json_path+".config","fs_laser_time")

		segments=self.bin.get_token_value(json_path+".mesh","segments")

		for seg in range(0,segments):
			length=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"len")
			end_time=pos+length

			dt=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"dt")
			if dt<=0.0:
				dt=length/10

			voltage_start=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"voltage_start")
			voltage_stop=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"voltage_stop")

			laser_start=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"laser_start")
			laser_stop=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"laser_stop")

			sun_start=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"sun_start")
			sun_stop=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"sun_stop")

			mul=self.bin.get_token_value(json_path+".mesh.segment"+str(seg),"mul")
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
		json_path=self.refind_json_path()
		start_time=fs_laser_time=self.bin.get_token_value(json_path+".config","start_time")

		new_time=dlg_get_text2( _("Enter the start time of the simulation"), str(start_time),"start.png")
		new_time=new_time.ret

		if new_time!=None:
			self.bin.set_token_value(json_path+".config","start_time",new_time)
			self.build_mesh()
			self.draw_graph()
			self.bin.save()




