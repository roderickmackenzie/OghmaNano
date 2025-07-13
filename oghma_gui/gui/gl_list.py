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
from bytes2str import str2bytes
from bytes2str import bytes2str
import ctypes
from json_c import json_tree_c

class gl_objects():

	def gl_object_deselect_all(self):
		self.lib.gl_objects_deselect_all(ctypes.byref(self.gl_main))

	def gl_objects_move_update_json(self):
		self.lib.gl_update_json(ctypes.byref(json_tree_c()), ctypes.byref(self.gl_main))
		self.bin.save()

	def gl_objects_select_by_id(self,in_id):
		self.lib.gl_objects_select_by_id(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes(in_id)))

	def gl_objects_search_by_color(self,r,g,b):
		number=0
		for n_obj in range(0,self.gl_main.objects_n):
			o=self.gl_main.get_object(n_obj)
			if o.match_false_color(r,g,b)==True:
				return o,number
			number=number+1
		return None,None

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




