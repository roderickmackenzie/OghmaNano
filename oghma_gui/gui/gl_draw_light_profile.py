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

## @package gl_draw_light_profile
#  Draw the 3D light profile
#

from OpenGL.GL import *
from OpenGL.GLU import *

from dat_file import dat_file
from epitaxy import get_epi

from vec import vec

from shape import shape
from cal_path import sim_paths
from json_root import json_root
from bytes2str import bytes2str
from bytes2str import str2bytes

class gl_draw_light_profile():

	def light_arrow_to_screen(self,source):
		import time
		a=self.gl_main.add_object()
		a.id=str2bytes(source.id)

		if source.light_illuminate_from=="xyz":
			for pos in source.expand_xyz0():
				xx=self.scale.project_m2screen_x(pos.x)
				yy=self.scale.project_m2screen_y(pos.y)
				zz=self.scale.project_m2screen_z(pos.z)
				a.add_xyz(xx,yy,zz)
				if source.shape_type!="box":
					break
			a.r=0.0
			a.g=1.0
			a.b=0.0
			a.rotate_x=source.rotate_x
			a.rotate_y=source.rotate_y

			a.moveable=True
			a.selectable=True

			if source.shape_type=="box":
				a.type=b"light_arrows"
				a.dx=0.5
				a.dy=0.5
				a.dz=0.5
			else:
				a.type=b"solid_and_mesh"
				a.dx=source.shape_nx*source.dx*self.gl_main.scale.x_mul
				a.dy=source.shape_ny*source.dy*self.gl_main.scale.y_mul
				a.dz=source.shape_nz*source.dz*self.gl_main.scale.z_mul

				block=a.add_block()
				block.gl_array_type=GL_LINES
				block.gl_line_width=5
				block.solid_lines=True
				self.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(source.triangles))
				self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(source.color_r*0.9), ctypes.c_float(source.color_g*0.9), ctypes.c_float(source.color_b*0.9), ctypes.c_float(source.color_alpha), ctypes.c_int(block.gl_array_points))

		else:
			data=json_root()
			a.type=b"solid_and_mesh"

			div=1.0
			if data.optical.light.Psun==0.0:
				return
			elif data.optical.light.Psun<=0.01:
				div=5
			elif data.optical.light.Psun<=0.1:
				div=8
			elif data.optical.light.Psun<=1.0:
				div=10
			elif data.optical.light.Psun<=10.0:
				div=20
			else:
				div=25

			dx=data.electrical_solver.mesh.mesh_x.get_len()/div
			dy=data.electrical_solver.mesh.mesh_y.get_len()/div
			dz=data.electrical_solver.mesh.mesh_z.get_len()/div

			x_start=dx/2.0
			y_start=dy/2.0
			z_start=dz/2.0

			x_stop=data.electrical_solver.mesh.mesh_x.get_len()
			y_stop=data.electrical_solver.mesh.mesh_y.get_len()
			z_stop=data.electrical_solver.mesh.mesh_z.get_len()

			x=x_start
			y=y_start
			z=z_start

			if source.light_illuminate_from.startswith("y"):
				a.dx=self.gl_main.scale.x_mul*data.electrical_solver.mesh.mesh_x.get_len()
				a.dy=1.5
				a.dz=self.gl_main.scale.z_mul*data.electrical_solver.mesh.mesh_z.get_len()

				xx=self.scale.project_m2screen_x(0)
				if source.light_illuminate_from=="y0":
					yy=self.scale.project_m2screen_y(self.gl_main.scale.world_min.y)-1.4
				elif source.light_illuminate_from=="y1":
					yy=self.scale.project_m2screen_y(self.gl_main.scale.world_max.y)
				zz=self.scale.project_m2screen_z(0)
				a.add_xyz(xx,yy,zz)

			elif source.light_illuminate_from.startswith("x"):
				a.dx=1.0
				a.dy=self.gl_main.scale.y_mul*data.epitaxy.ylen()
				a.dz=self.gl_main.scale.z_mul*data.electrical_solver.mesh.mesh_z.get_len()

				if source.light_illuminate_from=="x0":
					xx=self.scale.project_m2screen_x(self.gl_main.scale.world_min.x)-1.0
				elif source.light_illuminate_from=="x1":
					xx=self.scale.project_m2screen_x(self.gl_main.scale.world_max.x)+1.0
				yy=self.scale.project_m2screen_y(0)
				xz=self.scale.project_m2screen_z(0)
				a.add_xyz(xx,yy,zz)
			elif source.light_illuminate_from.startswith("z"):
				a.dx=self.gl_main.scale.x_mul*data.electrical_solver.mesh.mesh_x.get_len()
				a.dy=self.gl_main.scale.y_mul*data.epitaxy.ylen()
				a.dz=1.0

				xx=self.scale.project_m2screen_x(0)
				yy=self.scale.project_m2screen_y(0)
				if source.light_illuminate_from=="z0":
					zz=self.scale.project_m2screen_z(self.gl_main.scale.world_min.z)-1.0
				elif source.light_illuminate_from=="z1":
					zz=self.scale.project_m2screen_z(self.gl_main.scale.world_max.z)+1.0
				a.add_xyz(xx,yy,zz)

			a.r=0.0
			a.g=1.0
			a.b=0.0

			if source.light_illuminate_from=="y0":
				pass
			elif source.light_illuminate_from=="y1":
				a.rotate_x=180.0
			elif source.light_illuminate_from=="x0":
				a.rotate_y=90.0
				a.rotate_x=90.0
			elif source.light_illuminate_from=="x1":
				a.rotate_y=90.0
				a.rotate_x=90.0+180
			elif source.light_illuminate_from=="z0":
				a.rotate_y=0.0
				a.rotate_x=90.0
			elif source.light_illuminate_from=="z1":
				a.rotate_y=180.0
				a.rotate_x=90.0

			a.moveable=False
			a.selectable=False

			color=[0.0,1.0,0.0,1.0]

			block=a.add_block()
			block.gl_array_type=GL_LINES
			block.gl_line_width=4
			block.solid_lines=True
			self.lib.gl_photon_sheet(ctypes.byref(block),ctypes.c_float(div),ctypes.c_int(True))
			self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(color[0]), ctypes.c_float(color[1]), ctypes.c_float(color[2]), ctypes.c_float(color[3]), ctypes.c_int(block.gl_array_points))

			block=a.add_block()
			block.gl_array_type=GL_TRIANGLES
			block.gl_line_width=4
			block.solid_lines=True
			self.lib.gl_photon_sheet(ctypes.byref(block),ctypes.c_float(div),ctypes.c_int(False))
			self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(color[0]), ctypes.c_float(color[1]), ctypes.c_float(color[2]), ctypes.c_float(color[3]), ctypes.c_int(block.gl_array_points))



