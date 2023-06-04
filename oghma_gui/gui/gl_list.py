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

## @package gl_list
#  An object store from which the 3d scene is rendered
#

from vec import vec
from gl_base_object import gl_base_object
from json_root import json_root
from bytes2str import str2bytes
from bytes2str import bytes2str
import time
import ctypes

class gl_objects():

	def gl_object_deselect_all(self):
		self.lib.gl_objects_deselect_all(ctypes.byref(self.gl_main))

	def gl_objects_selected_min_max_vec(self):
		xyz_min=vec()
		xyz_max=vec()
		ret=self.lib.gl_objects_selected_min_max_vec(ctypes.byref(self.gl_main), ctypes.byref(xyz_min),ctypes.byref(xyz_max))
		if ret!=0:
			return False,False
		
		return xyz_min,xyz_max

	def gl_objects_rotate(self,rotate_x,rotate_y):
		self.lib.gl_objects_selected_rotate(ctypes.byref(self.gl_main),ctypes.c_float(rotate_x),ctypes.c_float(rotate_y))

	def gl_objects_move(self,dx,dy,dz):
		self.lib.gl_objects_selected_move(ctypes.byref(self.gl_main),ctypes.c_float(dx),ctypes.c_float(dy),ctypes.c_float(dz))

	def gl_objects_move_update_json(self):
		for n_obj in range(0,self.gl_main.objects_n):
			obj=self.gl_main.get_object(n_obj)
			if obj.selected==True:
					s=json_root().find_object_by_id(bytes2str(obj.id))
					if s!=None:
						if self.mouse_click_event.scale==True:
							if obj.resizable==True:
								s.dy=s.dy+self.mouse_click_event.dxyz.y/self.gl_main.scale.y_mul
								s.dx=s.dx+self.mouse_click_event.dxyz.x/self.gl_main.scale.x_mul
								s.dz=s.dz+self.mouse_click_event.dxyz.z/self.gl_main.scale.z_mul
						else:
							if obj.moveable==True:
								s.y0=s.y0+self.mouse_click_event.dxyz.y/self.gl_main.scale.y_mul
								s.x0=s.x0+self.mouse_click_event.dxyz.x/self.gl_main.scale.x_mul
								s.z0=s.z0+self.mouse_click_event.dxyz.z/self.gl_main.scale.z_mul

								s.rotate_x=s.rotate_x+self.mouse_click_event.rotate_x
								s.rotate_y=s.rotate_y+self.mouse_click_event.rotate_y

		json_root().save()

	def gl_objects_scale(self,dx,dy,dz):
		self.lib.gl_objects_selected_scale(ctypes.byref(self.gl_main),ctypes.c_float(dx),ctypes.c_float(dy),ctypes.c_float(dz))

	def gl_objects_remove_regex(self,in_id):
		self.lib.gl_main_object_delete_by_id(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes(in_id)))

	def gl_objects_select_by_id(self,in_id):
		self.lib.gl_objects_select_by_id(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes(in_id)))

	def gl_objects_search_by_color(self,r,g,b):
		for n_obj in range(0,self.gl_main.objects_n):
			o=self.gl_main.get_object(n_obj)
			if o.match_false_color(r,g,b)==True:
				return o
		return None

	def gl_objects_get_first_selected(self):
		for n_obj in range(0,self.gl_main.objects_n):
			o=self.gl_main.get_object(n_obj)
			if o.selected==True:
				return o
		return None

	def gl_objects_get_selected(self):
		ret=[]
		for n_obj in range(0,self.gl_main.objects_n):
			o=self.gl_main.get_object(n_obj)
			if o.selected==True:
				ret.append(o)
		return ret

	def gl_objects_clear(self):
		self.lib.gl_main_clear_objects(ctypes.byref(self.gl_main))

		for data in self.graph_data:
			data.plotted=False

		for data in self.ray_data:
			data.plotted=False

		for data in self.data_files:
			data.plotted=False

		self.stars_loaded=False

	def gl_objects_find(self,in_id):
		ret=self.lib.gl_objects_find(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes(in_id)))
		if ret==0:
			return None
		return gl_base_object.from_address(ret)


	def gl_objects_is_selected(self):
		for n_obj in range(0,self.gl_main.objects_n):
			o=self.gl_main.get_object(n_obj)
			if o.selected==True:
				return o
		return False
