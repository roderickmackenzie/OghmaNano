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

## @package gl
#  The main OpenGL display.
#

import ctypes
from dat_file import dat_file
from cal_path import sim_paths
from gl_base_object import gl_base_object
from vec import vec

class gl_simple_shapes_lib(ctypes.Structure):
	_fields_ = [('box', dat_file),
				('stars', dat_file),
				('optical_mode', dat_file)]

class gl_scale(ctypes.Structure):
	_fields_ = [('z_mul', ctypes.c_double),
				('x_mul', ctypes.c_double),
				('y_mul', ctypes.c_double),
				('z_start', ctypes.c_double),
				('x_start', ctypes.c_double),
				('y_start', ctypes.c_double),
				('gl_universe_x0', ctypes.c_double),
				('gl_universe_x1', ctypes.c_double),
				('gl_universe_z0', ctypes.c_double),
				('gl_universe_z1', ctypes.c_double),
				('world_fills_mesh', ctypes.c_int),
				('calculated_world_min_max', ctypes.c_int),
				('world_min', vec),
				('world_max', vec)]

class gl_text(ctypes.Structure):
	_fields_ = [('items', ctypes.c_void_p),
				('n_items', ctypes.c_int),
				('n_items_max', ctypes.c_int),
				('buf', ctypes.c_void_p),
				('library', ctypes.c_void_p),
				('face', ctypes.c_void_p)]

class gl_main(ctypes.Structure):
	_fields_ = [('objects_n', ctypes.c_int),
				('objects_max', ctypes.c_int),
				('objects', ctypes.c_void_p),
				('false_color', ctypes.c_int),
				('text', gl_text),
				('scale', gl_scale),
				('simple_shapes_lib', gl_simple_shapes_lib),
				('active_view', ctypes.c_void_p)]

	def __init__(self):
		self.lib=sim_paths.get_dll_py()
		self.lib.gl_main_add_object.restype = ctypes.c_void_p
		self.lib.gl_main_get_object.restype = ctypes.c_void_p
		self.lib.gl_base_object_add_block.restype = ctypes.c_void_p
		self.lib.gl_main_init(ctypes.byref(self))

	def __del__(self):
		self.lib.gl_main_free(ctypes.byref(self))

	def add_object(self):
		ret=gl_base_object.from_address(self.lib.gl_main_add_object(ctypes.byref(self)))
		ret.__init__()
		return ret

	def get_object(self,n):
		return gl_base_object.from_address(self.lib.gl_main_get_object(ctypes.byref(self),ctypes.c_int(n)))

