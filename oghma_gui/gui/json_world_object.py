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

## @package shape
#  Shape object file.
#

from vec import vec
from dat_file import dat_file
import os
from cal_path import sim_paths

class json_world_object():
	def __init__(self):
		self.var_list=[]
		self.var_list.append(["enabled",True])

		self.var_list.append(["text_object_",""])
		self.var_list.append(["x0",0.0])
		self.var_list.append(["y0",0.0])
		self.var_list.append(["z0",0.0])

		self.var_list.append(["dx",1e-9])
		self.var_list.append(["dy",1e-9])
		self.var_list.append(["dz",1e-9])

		self.var_list.append(["dx_padding",0.0])
		self.var_list.append(["dy_padding",0.0])
		self.var_list.append(["dz_padding",0.0])

		self.var_list.append(["shape_nx",1])
		self.var_list.append(["shape_ny",1])
		self.var_list.append(["shape_nz",1])

		self.var_list.append(["rotate_y",0.0])
		self.var_list.append(["rotate_x",0.0])

		self.var_list.append(["text_attributes_",""])

		self.var_list.append(["color_r",0.8])
		self.var_list.append(["color_g",0.8])
		self.var_list.append(["color_b",0.8])
		self.var_list.append(["color_alpha",0.8])

		self.var_list.append(["name","none"])
		self.var_list.append(["html_link",""])
		self.var_list.append(["label",""])
		self.var_list.append(["image_path",""])
		self.var_list.append(["shape_type","box"])

		#semiconductor gradients
		self.var_list.append(["g_x0",1.0])
		self.var_list.append(["g_y0",0.0])
		self.var_list.append(["g_x1",1.0])
		self.var_list.append(["g_y1",0.0])

		self.var_list.append(["id",self.random_id()])

		self.var_list_build()
		self.triangles=None
		self.shape_path=""

	def expand_xyz0(self):
		vectors=[]

		for x in range(0,self.shape_nx):
			for y in range(0,self.shape_ny):
				for z in range(0,self.shape_nz):
						pos=vec()
						pos.x=(self.x0+(self.dx+self.dx_padding)*x)
						pos.y=(self.y0+(self.dy+self.dy_padding)*y)
						pos.z=(self.z0+(self.dz+self.dz_padding)*z)

						vectors.append(pos)
						if self.enabled==False:
							break
		return vectors

	def rescale(self,rx,ry,rz):
		self.x0=self.x0*rx
		self.y0=self.y0*ry
		self.z0=self.z0*rz

		self.dx=self.dx*rx
		self.dy=self.dy*ry
		self.dz=self.dz*rz

		self.dx_padding=self.dx_padding*rx
		self.dy_padding=self.dy_padding*ry
		self.dz_padding=self.dz_padding*rz

	def load_triangles(self):
		self.shape_path=os.path.join(sim_paths.get_shape_path(),self.shape_type,"shape.inp")
		if os.path.isfile(self.shape_path)==True:
			self.triangles=dat_file()
			self.triangles.load(self.shape_path,raw_data=True)
			if self.triangles.data!=None:
				a=vec()
				min_vec=self.triangles.gl_triangles_get_min()
				self.triangles.gl_triangles_sub_vec(min_vec)
				max_vec=self.triangles.gl_triangles_get_max()
				self.triangles.gl_triangles_div_vec(max_vec)


	def get_min_max(self,my_min,my_max):
		#x
		if self.x0<my_min.x:
			my_min.x=self.x0
		if self.x0>my_max.x:
			my_max.x=self.x0

		if self.x0+self.dx<my_min.x:
			my_min.x=self.x0+self.dx
		if self.x0+self.dx>my_max.x:
			my_max.x=self.x0+self.dx

		#y
		if self.y0<my_min.y:
			my_min.y=self.y0
		if self.y0>my_max.y:
			my_max.y=self.y0

		if self.y0+self.dy<my_min.y:
			my_min.y=self.y0+self.dy
		if self.y0+self.dy>my_max.y:
			my_max.y=self.y0+self.dy

		#z
		if self.z0<my_min.z:
			my_min.z=self.z0
		if self.z0>my_max.z:
			my_max.z=self.z0

		if self.z0+self.dz<my_min.z:
			my_min.z=self.z0+self.dz
		if self.z0+self.dz>my_max.z:
			my_max.z=self.z0+self.dz

		return my_min,my_max
