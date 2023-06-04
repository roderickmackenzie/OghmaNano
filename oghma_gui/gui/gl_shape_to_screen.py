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

## @package gl_lib
#  general backend for the OpenGL viewer.
#


from OpenGL.GL import *
from OpenGL.GLU import *

import os
from vec import vec
from epitaxy import get_epi
from json_root import json_root
import time
from bytes2str import str2bytes

class shape_layer():

	def shape_to_screen(self,shape0,base_obj=None,epitaxy=False,z_shift=0.0):
		show=True
		z_mesh=json_root().electrical_solver.mesh.mesh_z
		x_mesh=json_root().electrical_solver.mesh.mesh_x
		a=self.gl_main.add_object()
		a.id=str2bytes(shape0.id)
		a.moveable=shape0.moveable
		hidden=False
		if shape0.enabled==False:
			hidden=True

		if shape0.display_options.hidden==True:
			hidden=True

		if shape0.display_options.show_solid==False and shape0.display_options.show_mesh==False:
			hidden=True

		if hidden==False:
			found=False
			if shape0.image_path!="":
				if os.path.isfile(shape0.image_path)==True:
					if shape0.image_path.endswith(".png"):
						a.type=b"image"
						a.image_path=shape0.image_path	
						found=True

			if found==False:
				a.type=b"solid_and_mesh"
							
		else:
			a.type=b"marker"
			#if self.active_view.show_buttons==False:
			#	show=False

		if show==True:
			for pos in shape0.expand_xyz0():

				if base_obj!=None:
					vec_base=vec()
					vec_base.x=base_obj.x0
					vec_base.y=base_obj.y0
					vec_base.z=base_obj.z0
					pos=pos+vec_base
				x=self.scale.project_m2screen_x(pos.x)
				y=self.scale.project_m2screen_y(pos.y)
				z=self.scale.project_m2screen_z(pos.z)+z_shift
				a.add_xyz(x,y,z)

			if x_mesh.get_points()==1 and z_mesh.get_points()==1 and epitaxy==True:
				a.dx=json_root().electrical_solver.mesh.mesh_x.get_len()*self.gl_main.scale.x_mul
				a.dy=shape0.dy*self.gl_main.scale.y_mul
				a.dz=json_root().electrical_solver.mesh.mesh_z.get_len()*self.gl_main.scale.z_mul
			else:
				a.dx=shape0.dx*self.gl_main.scale.x_mul
				a.dy=shape0.dy*self.gl_main.scale.y_mul
				a.dz=shape0.dz*self.gl_main.scale.z_mul

			a.r=shape0.color_r
			a.g=shape0.color_g
			a.b=shape0.color_b

			a.alpha=1.0
			if len(shape0.segments)>0:
				a.alpha=0.5

			a.allow_cut_view=True
			a.selectable=True

			a.rotate_x=shape0.rotate_x
			a.rotate_y=shape0.rotate_y

			#resize the shape to the mesh
			a.html=str2bytes(shape0.html_link)
			a.text=str2bytes(shape0.label)
			#print(a.text,a.type)
			slice_plane_x=-1e3
			slice_plane_y=-1e3
			if shape0.display_options.show_cut_through_x==True:
				slice_plane_x=0.5

			if shape0.display_options.show_cut_through_y==True:
				slice_plane_y=0.5

			if shape0.display_options.show_mesh==True:
				if shape0.triangles!=None:
					block=a.add_block()
					block.gl_array_type=GL_LINES
					block.gl_line_width=5
					block.solid_lines=True
					block.slice_plane_x=slice_plane_x
					block.slice_plane_y=slice_plane_y
					self.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(shape0.triangles))
					self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(shape0.color_r*0.9), ctypes.c_float(shape0.color_g*0.9), ctypes.c_float(shape0.color_b*0.9), ctypes.c_float(shape0.color_alpha), ctypes.c_int(block.gl_array_points))
					self.lib.gl_code_block_slice_triangles(ctypes.byref(block))

			if self.active_view.transparent_objects==False:
				if shape0.display_options.show_solid==True:
					if shape0.triangles!=None:
						block=a.add_block()
						block.gl_array_type=GL_TRIANGLES
						block.gl_line_width=5
						block.solid_lines=True
						block.slice_plane_x=slice_plane_x
						block.slice_plane_y=slice_plane_y
						self.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(shape0.triangles))
						self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(shape0.color_r), ctypes.c_float(shape0.color_g), ctypes.c_float(shape0.color_b), ctypes.c_float(shape0.color_alpha), ctypes.c_int(block.gl_array_points))
						self.lib.gl_code_block_slice_triangles(ctypes.byref(block))

		#now itterate over other shapes in this shape
		for s in shape0.segments:
			self.shape_to_screen(s,base_obj=shape0)






