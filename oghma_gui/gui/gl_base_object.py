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

## @package gl_base_object
#  Save the OpenGL scene.
#

from vec import vec
import ctypes
from cal_path import sim_paths


class code_block(ctypes.Structure):
	_fields_ = [('gl_array_type', ctypes.c_int ),
				('solid_lines', ctypes.c_int ),
				('gl_array_points', ctypes.c_int ),
				('gl_line_width', ctypes.c_int ),
				('gl_array_float32C', ctypes.POINTER(ctypes.c_float) ),
				('gl_array_colors_float32C', ctypes.POINTER(ctypes.c_float) ),
				('slice_plane_x', ctypes.c_float ),
				('slice_plane_y', ctypes.c_float ),
				('gl_point_size', ctypes.c_int )]


class gl_base_object(ctypes.Structure):
	OGHMA_GL_LIGHT=0
	OGHMA_GL_REAL_WORLD_OBJECT=1
	_fields_ = [('r', ctypes.c_float ),
				('g', ctypes.c_float ),
				('b', ctypes.c_float ),
				('alpha', ctypes.c_float ),
				('r_false', ctypes.c_float ),
				('g_false', ctypes.c_float ),
				('b_false', ctypes.c_float ),
				('rotate_y', ctypes.c_float ),
				('rotate_x', ctypes.c_float ),
				('xyz_max', ctypes.c_int ),
				('xyz_n', ctypes.c_int ),
				('xyz', ctypes.c_void_p ),
				('dx', ctypes.c_float ),
				('dy', ctypes.c_float ),
				('dz', ctypes.c_float ),
				('render_as', ctypes.c_char * 100),
				('selected', ctypes.c_int ),
				('moveable', ctypes.c_int ),
				('resizable', ctypes.c_int ),
				('selectable', ctypes.c_int ),
				('allow_cut_view', ctypes.c_int ),
				('text', ctypes.c_char * 4096 ),
				('text_size', ctypes.c_float ),
				('html', ctypes.c_char * 4096 ),
				('id', ctypes.c_char * 4096 ),
				('id1', ctypes.c_char * 4096 ),
				('image_path', ctypes.c_char * 4096 ),
				('blocks_n', ctypes.c_int ),
				('blocks_max', ctypes.c_int ),
				('blocks', ctypes.c_void_p ),
				('deleted', ctypes.c_int ),
				('image_buf', ctypes.POINTER(ctypes.c_char)),
				('image_w', ctypes.c_int),
				('image_h', ctypes.c_int),
				('texture', ctypes.c_int),
				('texture_used', ctypes.c_int),
				('object_type', ctypes.c_int),
				('inside', ctypes.c_int)]


	def match_false_color(self,r,g,b):
		if sim_paths.get_dll_py().gl_base_object_match_false_color(ctypes.byref(self),ctypes.c_float(r), ctypes.c_float(g), ctypes.c_float(b))==0:
			return True
		return False


