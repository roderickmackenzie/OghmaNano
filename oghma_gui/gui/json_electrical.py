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

## @package json_electrical
#  Store the cv domain json data
#


from json_base import json_base

class json_electrical(json_base):
	def __init__(self):
		json_base.__init__(self,"shape_electrical")
		self.var_list=[]
		self.var_list.append(["enabled",False])
		self.var_list.append(["electrical_component","resistance"])
		self.var_list.append(["electrical_shunt",1e6])
		self.var_list.append(["electrical_symmetrical_resistance","symmetric"])
		self.var_list.append(["electrical_series_z",0.24390])
		self.var_list.append(["electrical_series_x",0.24390])
		self.var_list.append(["electrical_series_y",1e-8])
		self.var_list.append(["electrical_n",1.2])
		self.var_list.append(["electrical_J0",0.5e-8])
		self.var_list.append(["electrical_enable_generation","False"])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()

