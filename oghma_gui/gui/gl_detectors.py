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

try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	pass
from json_root import json_root
from vec import vec
import ctypes
from bytes2str import str2bytes 
class gl_detectors():

	def add_detectors(self):
		if self.active_view.show_detectors==True:
			data=json_root()
			for shape in data.optical.detectors.segments:
				if shape.enabled==True:
					self.gl_objects_add_grid2(shape,nx=shape.viewpoint_nx,nz=shape.viewpoint_nz)


	def gl_objects_add_grid2(self,shape0,nx=8,nz=8):
		o=self.gl_main.add_object()
		o.id=str2bytes(shape0.id)
		o.type=b"solid_and_mesh"

		o.selectable=True
		o.moveable=True
		o.rotate_x=shape0.rotate_x
		o.rotate_y=shape0.rotate_y

		o.r=shape0.color_r
		o.g=shape0.color_g
		o.b=shape0.color_b

		o.dx=shape0.dx*self.gl_main.scale.x_mul
		o.dy=shape0.dy*self.gl_main.scale.y_mul
		o.dz=shape0.dz*self.gl_main.scale.z_mul

		dx=1.0/nx
		dz=1.0/nz

		xx=self.scale.project_m2screen_x(shape0.x0)
		zz=self.scale.project_m2screen_z(shape0.z0)
		yy=self.scale.project_m2screen_y(shape0.y0)

		o.add_xyz(xx,yy,zz)

		block=o.add_block()
		block.gl_array_type=GL_LINES
		block.gl_line_width=2
		block.solid_lines=True

		ny=0
		color=[shape0.color_r,shape0.color_g,shape0.color_b,1.0]
		self.lib.gl_code_bloc_gen_grid(ctypes.byref(block), ctypes.c_float(0.0),ctypes.c_float(1.0),ctypes.c_float(-1.0), ctypes.c_float(-1.0), ctypes.c_float(0.0), ctypes.c_float(1.0), ctypes.c_int(nx), ctypes.c_int(ny) , ctypes.c_int(nz))
		self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(color[0]), ctypes.c_float(color[1]), ctypes.c_float(color[2]), ctypes.c_float(color[3]), ctypes.c_int(block.gl_array_points))


