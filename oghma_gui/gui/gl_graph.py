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

## @package gl_graph
#  The gl_graph class for the OpenGL display.
#

import os
import sys
from math import fabs
from cal_path import sim_paths

from dat_file import dat_file
from vec import vec
from bytes2str import bytes2str
from bytes2str import str2bytes
try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	pass

import time

class gl_graph():

	def __init__(self):
		self.graph_data=[]

	def draw_graphs(self,graph_data,scale=True):

		for data in graph_data:
			if data.valid_data==True:				
				if data.type==b"3d":
					if self.active_view.render_plot==True:
						self.graph_project_3d_slice_to_image(data)
				elif data.type==b"rays":
					self.draw_graph_rays(data)
				elif data.type==b"poly":
					if scale==True:
						self.draw_graph_triangles_scale(data)
					else:
						self.draw_graph_triangles(data)
				elif data.type==b"3d-mesh":
					self.draw_graph_triangles(data,solid=False,gl_line_width=2,line_alpha=1.0)
				elif data.cols==b"zxyrgb":
					self.draw_graph_zxyrgb(data)
				elif data.cols==b"zxyzxyrgb":
					self.draw_graph_zxyzxyrgb(data)

	def graph_project_3d_slice_to_image(self,data):
		
		image_file=os.path.splitext(bytes2str(data.file_name))[0]+"_render.png"

		if len(data.y_scale)>1 and len(data.x_scale)>1 and len(data.z_scale)>1:
			print("can't project truly 3d images yet") 

		len_x=len(data.x_scale)
		len_y=len(data.y_scale)
		len_z=len(data.z_scale)

		zi=0

		z0=self.scale.project_m2screen_z(data.z_scale[0])
		z1=self.scale.project_m2screen_z(data.z_scale[len(data.z_scale)-1])
		x0=self.scale.project_m2screen_x(data.x_scale[0])
		x1=self.scale.project_m2screen_x(data.x_scale[len(data.x_scale)-1])
		y0=self.scale.project_m2screen_y(data.y_scale[0])
		y1=self.scale.project_m2screen_y(data.y_scale[len(data.y_scale)-1])

		o=self.gl_objects_find("graph_"+data.id)
		if o==None:
			o=self.gl_main.add_object()
			self.lib.gl_base_object_insert_rgba(ctypes.byref(o),ctypes.byref(data))

			o.add_xyz(x0,y0,z0)

			o.dx=x1-x0
			o.dy=y1-y0
			o.dz=z1-z0
			o.id=str2bytes("graph_"+bytes2str(data.id))
			o.type=str2bytes("image")
			o.image_path=str2bytes(image_file)

	def draw_mode(self):
		path=os.path.join(sim_paths.get_sim_path(),"optical_output","photons_yl_norm.csv")
		self.lib.gl_optical_mode(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes(path)))


