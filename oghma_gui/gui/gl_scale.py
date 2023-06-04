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

## @package gl_scale
#  The gl_scale class for the OpenGL display.
#

from json_root import json_root
import ctypes
from cal_path import sim_paths
from gl_main import gl_main

class gl_scale_class(ctypes.Structure):

	def __init__(self,gl_scale):
		self.gl_scale=gl_scale
		self.refresh_world_size=True
		self.world_delta=None
		self.lib=sim_paths.get_dll_py()
		self.lib.project_m2screen_x.restype = ctypes.c_float
		self.lib.project_m2screen_y.restype = ctypes.c_float
		self.lib.project_m2screen_z.restype = ctypes.c_float

	def project_m2screen_x(self,x):
		return self.lib.project_m2screen_x(ctypes.byref(self.gl_scale),ctypes.c_float(x))

	def project_m2screen_y(self,y):
		return self.lib.project_m2screen_y(ctypes.byref(self.gl_scale),ctypes.c_float(y))

	def project_m2screen_z(self,z):
		return self.lib.project_m2screen_z(ctypes.byref(self.gl_scale),ctypes.c_float(z))
		
	def set_m2screen(self):
		if self.refresh_world_size==True:
			wmin,wmax=json_root().get_world_size()
			self.world_delta=wmax-wmin
			self.gl_scale.world_min.x=wmin.x
			self.gl_scale.world_min.y=wmin.y
			self.gl_scale.world_min.z=wmin.z

			self.gl_scale.world_max.x=wmax.x
			self.gl_scale.world_max.y=wmax.y
			self.gl_scale.world_max.z=wmax.z

		self.gl_scale.world_fills_mesh=json_root().world.config.world_fills_mesh
		self.lib.set_m2screen(ctypes.byref(self.gl_scale))

