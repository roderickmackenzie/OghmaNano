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

## @package gl_lib_ray
#  Library to draw ray
#


from vec import vec
import ctypes
import time

try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	pass

class gl_lib_ray():

	def __init__(self):
		self.ray_data=[]

	def draw_graph_rays(self,data):
		if data.plotted==True:
			return

		o=self.gl_main.add_object()

		o.id=b"ray_trace"
		o.type=b"solid_and_mesh"

		o.add_xyz(0.0,0.0,0.0)

		block=o.add_block()
		block.gl_array_type=GL_LINES
		block.gl_line_width=4
		block.solid_lines=self.active_view.ray_solid_lines
		data.lib.gl_code_block_import_dat_file_ray(ctypes.byref(block),ctypes.byref(data))
		data.lib.gl_project_m2screen_zxy(ctypes.byref(block),ctypes.byref(self.gl_main.scale))


		data.plotted=True

	def draw_graph_triangles_scale(self,data):
		if data.plotted==True:
			return
		a=self.gl_main.add_object()
		a.id=b"graph_mesh"
		a.type=b"solid_and_mesh"

		xx=self.scale.project_m2screen_x(self.gl_main.scale.world_min.x)
		yy=self.scale.project_m2screen_y(self.gl_main.scale.world_min.y)
		zz=self.scale.project_m2screen_z(self.gl_main.scale.world_min.z)
		a.add_xyz(xx,yy,zz)

		a.dx=(self.gl_main.scale.world_max.x-self.gl_main.scale.world_min.x)*self.gl_main.scale.x_mul
		a.dy=(self.gl_main.scale.world_max.y-self.gl_main.scale.world_min.y)*self.gl_main.scale.y_mul
		a.dz=(self.gl_main.scale.world_max.z-self.gl_main.scale.world_min.z)*self.gl_main.scale.z_mul

		a.r=1.0
		a.g=0.0
		a.b=0.0
		a.selected=False
		a.moveable=False
		a.resizable=False
		a.rotate_x=180

		block=a.add_block()
		block.gl_array_type=GL_LINES
		block.gl_line_width=4
		block.solid_lines=self.active_view.ray_solid_lines
		data.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(data))
		data.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(a.r*0.9), ctypes.c_float(a.g*0.9), ctypes.c_float(a.b*0.9), ctypes.c_float(0.5), ctypes.c_int(block.gl_array_points))

		block=a.add_block()
		block.gl_array_type=GL_TRIANGLES
		block.gl_line_width=4
		block.solid_lines=self.active_view.ray_solid_lines
		data.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(data))
		data.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(a.r), ctypes.c_float(a.g), ctypes.c_float(a.b), ctypes.c_float(1.0), ctypes.c_int(block.gl_array_points))

		data.plotted=True

	def draw_graph_triangles(self,data,solid=True,gl_line_width=2,line_alpha=0.5):
		if data.plotted==True:
			return
		a=self.gl_main.add_object()
		a.id=b"bing"
		a.type=b"from_array"
		a.r=data.r
		a.g=data.g
		a.b=data.b
		a.add_xyz(0.0,0.0,0.0)
		block=a.add_block()
		block.gl_array_type=GL_LINES
		block.gl_line_width=gl_line_width
		block.solid_lines=self.active_view.ray_solid_lines
		data.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(data))
		data.lib.gl_project_m2screen_zxy(ctypes.byref(block),ctypes.byref(self.gl_main.scale))
		data.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(a.r*0.9), ctypes.c_float(a.g*0.9), ctypes.c_float(a.b*0.9), ctypes.c_float(line_alpha), ctypes.c_int(block.gl_array_points))

		if solid==True:
			block=a.add_block()
			block.gl_array_type=GL_TRIANGLES
			block.gl_line_width=2
			block.solid_lines=self.active_view.ray_solid_lines
			data.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(data))
			data.lib.gl_project_m2screen_zxy(ctypes.byref(block),ctypes.byref(self.gl_main.scale))
			data.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(a.r), ctypes.c_float(a.g), ctypes.c_float(a.b), ctypes.c_float(1.0), ctypes.c_int(block.gl_array_points))

		data.plotted=True

	def draw_graph_zxyzxyrgb(self,data):
		if data.plotted==True:
			return

		o=self.gl_main.add_object()

		o.id=b"ray_trace"
		o.type=b"from_array"

		o.add_xyz(0.0,0.0,0.0)

		block=o.add_block()
		block.gl_array_type=GL_LINES
		block.gl_line_width=4
		block.solid_lines=self.active_view.ray_solid_lines
		data.lib.gl_code_block_import_zxyzxyrgb(ctypes.byref(block),ctypes.byref(data))
		data.lib.gl_project_m2screen_zxy(ctypes.byref(block),ctypes.byref(self.gl_main.scale))


		data.plotted=True

	def draw_graph_zxyrgb(self,data):
		if data.plotted==True:
			return

		o=self.gl_main.add_object()

		o.id=b"ray_trace"
		o.type=b"from_array"

		o.add_xyz(0.0,0.0,0.0)

		block=o.add_block()
		block.gl_array_type=GL_POINTS
		block.gl_point_size=2
		block.solid_lines=self.active_view.ray_solid_lines
		data.lib.gl_code_block_import_zxyrgb(ctypes.byref(block),ctypes.byref(data))
		data.lib.gl_project_m2screen_zxy(ctypes.byref(block),ctypes.byref(self.gl_main.scale))


		data.plotted=True
