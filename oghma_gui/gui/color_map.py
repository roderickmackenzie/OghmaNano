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

## @package colors
#  Functions to deal with colors.
#

import ctypes
from cal_path import sim_paths
from PySide2.QtGui import QColor
from bytes2str import bytes2str
from bytes2str import str2bytes

class rgb_char(ctypes.Structure):
	_fields_ = [('r', ctypes.c_ubyte),
				('g', ctypes.c_ubyte),
				('b', ctypes.c_ubyte),
				('alpha', ctypes.c_ubyte)]

class color_map_item(ctypes.Structure):
    _fields_ = [("a", ctypes.POINTER(ctypes.c_ubyte)),
				("text", ctypes.c_char * 100),
				("len", ctypes.c_int)]

class color_map():

	def __init__(self):
		self.lib=sim_paths.get_dll_py()
		self.lib.color_map_find_by_name.restype = ctypes.POINTER(color_map_item)
		self.lib.color_map_find_random.restype = ctypes.POINTER(color_map_item)
		self.map=None

	def find_map(self,map_name):
		self.map=self.lib.color_map_find_by_name(ctypes.c_char_p(str2bytes(map_name)))

	def find_random_map(self):
		self.map=self.lib.color_map_find_random()

	def get_color(self,frac):
		rgb = rgb_char()
		self.lib.color_map_get_color2(ctypes.byref(rgb),ctypes.c_double(frac), self.map, ctypes.c_int(True))
		return rgb.r, rgb.g, rgb.b

	def get_color_exact(self,n,hex=False):
		rgb = rgb_char()
		self.lib.color_map_get_color2(ctypes.byref(rgb),ctypes.c_double(n), self.map, ctypes.c_int(False))
		#print(rgb.r, rgb.g, rgb.b)
		if hex==True:
			return '#%02x%02x%02x' % (rgb.r, rgb.g, rgb.b)
		return rgb.r, rgb.g, rgb.b

	def get_color_QColor(self,frac):
		rgb = rgb_char()
		self.lib.color_map_get_color2(ctypes.byref(rgb),ctypes.c_double(frac), self.map, ctypes.c_int(True))
		return QColor(rgb.r, rgb.g, rgb.b)

	def get_marker(self,i):
		return ""

	def get_color_names(self):
		names=ctypes.create_string_buffer(400)
		self.lib.color_map_get_colors(names)
		ret=bytes2str(names.value).split("\n")
		return ret

	def gen(self,n):
		ret=[]
		rgb = rgb_char()
		frac=0
		df=1.0/(float(n))
		for i in range(0,n):
			self.lib.color_map_get_color2(ctypes.byref(rgb),ctypes.c_double(frac), ctypes.c_int(self.map), ctypes.c_int(True))
			ret.append([rgb.r, rgb.g, rgb.b])
			frac=frac+df
		return ret
