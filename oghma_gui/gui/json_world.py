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

## @package json_world
#  Store the cv domain json data
#

from json_base import json_base
from shape import shape

class json_world_config(json_base):

	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["world_automatic_size",True])
		self.var_list.append(["world_fills_mesh",False])
		self.var_list.append(["world_x0",-1e-3])
		self.var_list.append(["world_x1",1e-3])
		self.var_list.append(["world_y0",-1e-3])
		self.var_list.append(["world_y1",1e-3])
		self.var_list.append(["world_z0",-1e-3])
		self.var_list.append(["world_z1",1e-3])
		self.var_list.append(["world_margin_x0",1.1])
		self.var_list.append(["world_margin_x1",1.1])
		self.var_list.append(["world_margin_y0",1.1])
		self.var_list.append(["world_margin_y1",1.5])
		self.var_list.append(["world_margin_z0",1.1])
		self.var_list.append(["world_margin_z1",1.1])

		self.var_list_build()

class json_world_data(json_base):

	def __init__(self):
		json_base.__init__(self,"world_data",segment_class=True)

	def load_from_json(self,json):
		self.segments=[]
		segs=json['segments']
		for i in range(0,segs):
			a=shape()
			simulation_name="segment"+str(i)
			a.load_from_json(json[simulation_name])
			self.segments.append(a)

class json_world(json_base):

	def __init__(self):
		json_base.__init__(self,"world")
		self.var_list=[]
		self.var_list.append(["config",json_world_config()])
		self.var_list.append(["world_data",json_world_data()])
		self.var_list_build()

