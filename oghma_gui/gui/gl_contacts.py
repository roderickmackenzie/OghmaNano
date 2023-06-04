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


try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	pass

from epitaxy import get_epi
from vec import vec

from json_root import json_root
from bytes2str import str2bytes

class gl_contacts():

	def draw_contacts(self,z_shift=0.0):
		epi=get_epi()
		box=vec()
		pos=vec()
		json_root().electrical_solver.mesh.mesh_y
		mesh_x=json_root().electrical_solver.mesh.mesh_x
		mesh_z=json_root().electrical_solver.mesh.mesh_z

		self.gl_objects_remove_regex("contact")
		top_contact_layer=epi.get_top_contact_layer()
		epi.get_btm_contact_layer()

		for c in epi.contacts.segments:
			if c.enabled==True:
				a=self.gl_main.add_object()
				a.id=str2bytes(c.id)
				added=False

				if c.position=="left" or c.position=="right":
					if mesh_x.enabled==True:
						sticking_out_bit=0.2
						a.type=b"solid_and_mesh"

						if c.position=="left":
							xx=self.scale.project_m2screen_x(0)-sticking_out_bit
						else:
							xx=self.scale.project_m2screen_x(mesh_x.get_len())

						yy=self.scale.project_m2screen_y(c.x0)
						zz=self.scale.project_m2screen_z(0)
						o.add_xyz(xx,yy,zz)

						a.dx=sticking_out_bit
						a.dy=self.gl_main.scale.y_mul*c.dx
						a.dz=self.gl_main.scale.z_mul*mesh_z.get_len()

						a.r=c.color_r
						a.g=c.color_g
						a.b=c.color_b
						a.coloralpha=1.0

						added=True

				elif c.position=="top" or c.position=="bottom":
					if top_contact_layer!=-1:

						if mesh_x.enabled==False:
							yy=0.0	#was missing from origonal
							xx=self.scale.project_m2screen_x(0.0)
							zz=self.scale.project_m2screen_z(0.0)
							a.dx=mesh_x.get_len()*self.gl_main.scale.x_mul
							
							#xyz.x=self.scale.project_m2screen_x(pos.x)
							#xyz.y=self.scale.project_m2screen_y(pos.y)
							zz=self.scale.project_m2screen_z(pos.z)
							a.add_xyz(xx,yy,zz)
						else:
							a.dx=c.dx*self.gl_main.scale.x_mul

						if mesh_z.enabled==False:
							a.dz=mesh_z.get_len()*self.gl_main.scale.z_mul
						else:
							a.dz=c.dz*self.gl_main.scale.z_mul

						if mesh_x.enabled==True or mesh_z.enabled==True:
							a.xyz_n=0
							for pos in c.expand_xyz0():
								xx=self.scale.project_m2screen_x(pos.x)
								yy=self.scale.project_m2screen_y(pos.y)
								zz=self.scale.project_m2screen_z(pos.z)+z_shift
								a.add_xyz(xx,yy,zz)

						added=True

						#fixup
						for n in range(0,a.xyz_n): 
							xyz=a.get_xyz(n)
							if c.position=="top":
								a.dy=epi.layers[0].dy*self.gl_main.scale.y_mul
								xyz.y=self.scale.project_m2screen_y(epi.get_layer_start(0))
							else:
								a.dy=epi.layers[len(epi.layers)-1].dy*self.gl_main.scale.y_mul
								xyz.y=self.scale.project_m2screen_y(epi.get_layer_start(len(epi.layers)-1))
							a.set_xyz(n,xyz)

				if added==True:
					a.type=b"solid_and_mesh"
					a.selectable=True

					a.r=c.color_r
					a.g=c.color_g
					a.b=c.color_b
					a.color_alpha=c.color_alpha

					a.rotate_x=c.rotate_x
					a.rotate_y=c.rotate_y

					if c.triangles!=None:
						block=a.add_block()
						block.gl_array_type=GL_LINES
						block.gl_line_width=5
						block.solid_lines=True
						self.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(c.triangles))
						self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(a.r*0.9), ctypes.c_float(a.g*0.9), ctypes.c_float(a.b*0.9), ctypes.c_float(a.color_alpha), ctypes.c_int(block.gl_array_points))

						block=a.add_block()
						block.gl_array_type=GL_TRIANGLES
						block.gl_line_width=5
						block.solid_lines=True
						self.lib.gl_code_block_import_dat_file_triangles(ctypes.byref(block),ctypes.byref(c.triangles))
						self.lib.gl_code_block_import_rgb(ctypes.byref(block),ctypes.c_float(a.r), ctypes.c_float(a.g), ctypes.c_float(a.b), ctypes.c_float(a.color_alpha), ctypes.c_int(block.gl_array_points))





