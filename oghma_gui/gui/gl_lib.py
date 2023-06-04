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

try:
	from OpenGL.GLU import *
	from OpenGL.GL import *
except:
	pass
import ctypes
from bytes2str import str2bytes

class gl_lib():

	def render_text(self,x,y,z,text,size_mul=1.0):
		obj = None
		self.lib.gl_draw_text(ctypes.byref(self.gl_main), ctypes.byref(obj), ctypes.c_char_p(str2bytes(text)), ctypes.c_char_p(str2bytes("")), ctypes.c_float(x), ctypes.c_float(y), ctypes.c_float(z), ctypes.c_float(size_mul))

	def set_false_color(self,value):
		self.gl_main.false_color=value
		if self.gl_main.false_color==True:
			glDisable(GL_LIGHTING)
		else:
			glEnable(GL_LIGHTING)

	def set_color(self,obj):
		self.lib.gl_set_color(ctypes.byref(obj),ctypes.c_int(self.gl_main.false_color))
