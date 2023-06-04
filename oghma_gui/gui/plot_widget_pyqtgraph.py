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

## @package plot_widget
#  The main plot widget.
#

from __future__ import unicode_literals

import os
from numpy import *

from util_latex import latex
from util import pygtk_to_latex_subscript
from color_map import get_color
from color_map import get_color_black
from color_map import get_marker
from util import fx_with_units
from util import time_with_units
from lock import get_lock
from sim_name import sim_name
import pyqtgraph as pg
import numpy as np
from color_map import color_map
from bytes2str import bytes2str

class plot_widget_pyqtgraph():

	def pyqtgraph_do_plot(self):
		if len(self.data)==0:
			return
		if self.data[0].valid_data==False:
			return

		if self.data[0].type=="poly":
			return

		key_text=[]

		self.plot_type=""

		if self.data[0].type==b"rgb":
			self.plot_type="rgb"
		elif self.data[0].type==b"quiver":
			self.plot_type="quiver"
		else:
			if self.data[0].x_len==1 and self.data[0].z_len==1:
				self.plot_type="linegraph"
			elif self.data[0].x_len>1 and self.data[0].y_len>1 and self.data[0].z_len==1:
				if self.data[0].type==b"3d":
					self.plot_type="wireframe"
				if self.data[0].type==b"heat":
					self.plot_type="heat"
			elif self.data[0].x_len>1 and self.data[0].y_len==1 and self.data[0].z_len>1:
				if self.data[0].type==b"3d":
					self.plot_type="wireframe"
				if self.data[0].type==b"heat":
					self.plot_type="heat"
			elif self.data[0].x_len==1 and self.data[0].y_len>1 and self.data[0].z_len>1:
				if self.data[0].type==b"3d":
					self.plot_type="wireframe"
				if self.data[0].type==b"heat":
					self.plot_type="heat"
			elif self.data[0].x_len>1 and self.data[0].y_len>1 and self.data[0].z_len>1:
				print("ohhh full 3D")
				self.plot_type="3d"
			else:
				print(_("I don't know how to process this type of file!"),self.data[0].x_len, self.data[0].y_len,self.data[0].z_len)
				return

		my_max=1.0

		self.canvas.clear()
		
		if self.plot_type=="linegraph":		#This is for the 1D graph case
			self.canvas.addLegend()

			force_log_data=False
			for d in self.data:
				try:
					if max(d.data[0][0])>1e15:
						force_log_data=True
				except:
					pass
			self.canvas.setLabel('bottom', bytes2str(self.data[0].y_label)+" ("+bytes2str(self.data[0].y_units)+")", color='k')
			self.canvas.setLabel('left', bytes2str(self.data[0].data_label)+" ("+bytes2str(self.data[0].data_units)+")", color='k')
			self.canvas.getAxis('bottom').enableAutoSIPrefix(False)
			self.canvas.getAxis('left').enableAutoSIPrefix(False)
			#self.canvas.setLogMode(False, True)
			pi = self.canvas.getPlotItem()
			if self.data[0].logy==True:
				ai = pi.getAxis("bottom")
				ai.setLogMode(True)

			if self.data[0].logdata==True or force_log_data==True:
				ai = pi.getAxis("left")
				ai.setLogMode(True)


			for d in self.data:
				if d.x_len==1 and d.z_len==1 and d.y_len>0:
					if d.rgb_to_hex()!=None:
						r=d.r
						g=d.g
						b=d.b
					else:
						r,g,b=get_color(self.data.index(d))

					r=int(r*255)
					g=int(g*255)
					b=int(b*255)
					name=""
					#self.canvas.setYRange(0.0,2e23)
					if d.key_text!="":
						name=d.key_text
						if d.key_units!="":
							name=name+" ("+d.key_units+")"
					
					pen=pg.mkPen((r, g, b), width=3)
					points=d.data[0][0]
					if self.data[0].logdata==True or force_log_data==True:
						points=list(map(abs, points))

					self.canvas.plot(x=d.y_scale, y=points, pen=pen, name=name )

					if len(d.labels)!=0:
						print("Not yet supported")

			self.canvas.setLogMode(self.data[0].logy, self.data[0].logdata or force_log_data)	#check out fxexperiment if does not work

		elif self.plot_type=="wireframe":
			print("Not yet supported")
		elif self.plot_type=="heat":
			colors = color_map(map_name="matlab_jet").map
			# color map
			cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, len(colors)), color=colors)

			# prepare demonstration data:
			data=np.array(self.data[0].data[0]).transpose()
			y_min=self.data[0].y_scale[0]
			y_max=self.data[0].y_scale[-1]

			x_min=self.data[0].x_scale[0]
			x_max=self.data[0].x_scale[-1]

			y_mul=(y_max-y_min)/len(self.data[0].y_scale)
			x_mul=(x_max-x_min)/len(self.data[0].x_scale)
			self.canvas.setImage(data, pos=[y_min,x_min], scale=[y_mul, x_mul],xvals=self.data[0].y_scale)

			self.canvas.setColorMap(cmap)
			self.plot_item.setAspectLocked(False)
			#self.canvas.adjustSize()
			self.plot_item.getAxis("left").setTextPen((0, 0, 0))
			self.plot_item.getAxis("bottom").setTextPen((0, 0, 0))
			self.plot_item.setLabel(axis='left', text=bytes2str(self.data[0].x_label)+" ("+bytes2str(self.data[0].x_units)+")")
			self.plot_item.setLabel(axis='bottom', text=bytes2str(self.data[0].y_label)+" ("+bytes2str(self.data[0].y_units)+")")
			self.plot_item.setLimits(xMin=y_min, xMax=y_max, yMin=x_min, yMax=x_max)
			vbox = self.canvas.getView()
			#.adjustSize()
		elif self.plot_type=="3d":
			print("Not yet supported")
		elif self.plot_type=="rgb":
			print("Not yet supported")



		#if get_lock().encode_output==True:
		#	x=0.8
		#	y=0.25
			#while(x<1.0):
			#	y=0
			#	while(y<1.0):
		#	self.fig.text(x, y, "Upgrade to "+sim_name.name+" professional today!", fontsize=20, color='gray', ha='right', va='bottom', alpha=0.05)

			#		y=y+0.2
			#	x=x+0.4

