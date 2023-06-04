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

## @package gl_cords
#  The gl_cords class for the OpenGL display.
#

from math import fabs

try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	pass

from vec import vec
import ctypes
from bytes2str import str2bytes

class gl_cords():

	def draw_cords(self):
		if self.gl_main.scale.calculated_world_min_max==False:
			return

		start_x=self.scale.gl_scale.gl_universe_x0+2
		start_z=self.scale.gl_scale.gl_universe_z0+2
		start_y=self.scale.project_m2screen_y(self.gl_main.scale.world_max.y)-2.0
		self.lib.gl_cords(ctypes.byref(self.gl_main), ctypes.c_float(start_x), ctypes.c_float(start_y), ctypes.c_float(start_z))

	def draw_numbers(self):
		self.render_text (self.gl_main,0.0,0.0,0.0, "(0,0,0)")
		self.render_text (self.gl_main,1.0,0.0,0.0, "(1,0,0)")
		self.render_text (self.gl_main,0.0,2.0,0.0, "(0,1,0)")
		self.render_text (self.gl_main,0.0,0.0,1.0, "(0,0,1)")

	#This should be replaced with gl_objects_add_grid2
	def gl_objects_add_grid(self,x0,x1,y0,y1,z0,z1,uid,color=[0.8,0.8,0.8,1.0],direction="zx"):
		o=self.gl_main.add_object()
		o.id=str2bytes(uid)
		o.type=b"solid_and_mesh"

		o.add_xyz(x0,y0,z0)
		o.text_size=1.0
		block=o.add_block()
		block.gl_array_type=GL_LINES
		block.gl_line_width=1
		block.solid_lines=True

		if direction=="zx":
			o.dx=x1-x0
			o.dz=z1-z0
			o.dy=0.0
			nx=40
			ny=0
			nz=40
		elif direction=="zy":
			o.dx=0.0
			o.dz=z1-z0
			o.dy=y1-y0
			nx=0
			ny=40
			nz=40
		elif direction=="xy":
			o.dx=x1-x0
			o.dz=0.0
			o.dy=y1-y0
			nx=40
			ny=40
			nz=0

		self.lib.gl_code_bloc_gen_grid(ctypes.byref(block), ctypes.c_float(0.0),ctypes.c_float(1.0),ctypes.c_float(0.0), ctypes.c_float(1.0), ctypes.c_float(0.0), ctypes.c_float(1.0),  ctypes.c_int(nx), ctypes.c_int(ny) , ctypes.c_int(nz))
		self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(color[0]), ctypes.c_float(color[1]), ctypes.c_float(color[2]), ctypes.c_float(color[3]), ctypes.c_int(block.gl_array_points))



	def world_box(self):
		self.gl_objects_remove_regex("world_box")
		a=self.gl_main.add_object()
		a.type=b"solid_and_mesh"
		a.id=b"world_box"

		xx=self.scale.project_m2screen_x(self.gl_main.scale.world_min.x)
		yy=self.scale.project_m2screen_y(self.gl_main.scale.world_min.y)
		zz=self.scale.project_m2screen_z(self.gl_main.scale.world_min.z)
		a.add_xyz(xx,yy,zz)

		a.dx=fabs(self.gl_main.scale.world_max.x-self.gl_main.scale.world_min.x)*self.gl_main.scale.x_mul
		a.dy=fabs(self.gl_main.scale.world_max.y-self.gl_main.scale.world_min.y)*self.gl_main.scale.y_mul
		a.dz=fabs(self.gl_main.scale.world_max.z-self.gl_main.scale.world_min.z)*self.gl_main.scale.z_mul

		a.r=1.0
		a.g=0.0
		a.b=0.0
		a.alpha=1.0

		block=a.add_block()
		block.gl_array_type=GL_LINES
		block.gl_line_width=5
		block.solid_lines=True
		self.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(self.default_shapes.box))
		self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(1.0), ctypes.c_float(0.0), ctypes.c_float(0.0), ctypes.c_float(1.0), ctypes.c_int(block.gl_array_points))



