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

## @package json_opengl_config
#  Store the cv domain json data
#

from json_base import json_base
from json_gl import json_gl_view

class json_opengl_config(json_base):

	def __init__(self):
		json_base.__init__(self,"opengl")
		self.var_list=[]
		self.var_list.append(["gl_dy_layer_offset",0.1])
		self.var_list.append(["gl_device_height",1.4])
		self.var_list.append(["gl_render_text",True])
		self.var_list.append(["color_r",0.8])		#background color
		self.var_list.append(["color_g",0.8])
		self.var_list.append(["color_b",0.8])
		self.var_list.append(["color_alpha",0.8])
		self.var_list.append(["render_grid",True])
		self.var_list.append(["gl_view",json_gl_view()])
		self.var_list_build()

