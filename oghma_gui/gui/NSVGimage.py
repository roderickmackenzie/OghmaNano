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

## @package gtkswitch
#  Package to provide an equivlent to the gnome switch
#


import os
from cal_path import sim_paths
from bytes2str import bytes2str
from bytes2str import str2bytes
from math import cos, sin
import ctypes

class NSVGpath(ctypes.Structure):

	def rotate(self,x_in,y_in,theta):
		theta_rad=(theta/360.0)*2*3.14159
		x=x_in*cos(theta_rad)-y_in*sin(theta_rad)
		y=x_in*sin(theta_rad)+y_in*cos(theta_rad)
		return x,y

NSVGpath._fields_ = [('pts', ctypes.POINTER(ctypes.c_float)),
					('npts', ctypes.c_int),
					('closed', ctypes.c_char),
					('bounds', ctypes.c_float *4),
					('next', ctypes.POINTER(NSVGpath))]

class NSVGpaint_u(ctypes.Union):
	_fields_ = [('color', ctypes.c_uint),
				('gradient', ctypes.c_void_p)]

class NSVGpaint(ctypes.Structure):
	_fields_ = [('type', ctypes.c_char),
				('color', NSVGpaint_u)]

class NSVGshape(ctypes.Structure):
	pass


NSVGshape._fields_ = [('id', ctypes.c_char * 64),
					('fill', NSVGpaint),
					('stroke', NSVGpaint),
					('opacity', ctypes.c_float),
					('strokeWidth', ctypes.c_float),
					('strokeDashOffset', ctypes.c_float),
					('strokeDashArray', ctypes.c_float * 8),
					('strokeDashCount', ctypes.c_char),
					('strokeLineJoin', ctypes.c_char),
					('strokeLineCap', ctypes.c_char),
					('miterLimit', ctypes.c_float),
					('fillRule', ctypes.c_char),
					('flags', ctypes.c_char),
					('bounds', ctypes.c_float * 4),
					('fillGradient', ctypes.c_char * 64),
					('strokeGradient', ctypes.c_char * 64),
					('xform', ctypes.c_float * 6),
					('paths', ctypes.POINTER(NSVGpath)),
					('next', ctypes.POINTER(NSVGshape))]


class NSVGimage(ctypes.Structure):

	def __init__(self):
		self.p=None
		self.b=""
		self.lib=sim_paths.get_dll_py()
		self.lib.svg_load.restype = ctypes.POINTER(NSVGimage)
		self.lib.svg_get_rgb.argtypes = (ctypes.POINTER(NSVGshape),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),)

	def load(self,file_name):
		if os.path.isfile(file_name)==True:
			self.p = ctypes.POINTER(NSVGimage)
			self.p=self.lib.svg_load(bytes(file_name, encoding='utf8'))

	def norm(self,dx,dy):
		self.lib.svg_norm(self.p,ctypes.c_float(dx),ctypes.c_float(dy))

	def free(self):
		if hasattr(self, 'p'):
			if self.p!=None:
				self.lib.svg_free(self.p)
				self.p=None
				#print("free",self.b)

	def __del__(self):
		#print("__del__")
		self.free()



NSVGimage._fields_ = [('width', ctypes.c_float),
				('height', ctypes.c_float),
				('shapes', ctypes.POINTER(NSVGshape))]
