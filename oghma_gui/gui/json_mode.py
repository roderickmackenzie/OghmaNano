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

## @package json_transfer_matrix
#  Store the cv domain json data
#


from json_base import json_base

class json_mode_config(json_base):

	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["mode_max_ittr",25])
		self.var_list.append(["mode_stop_error",10.0])
		self.var_list.append(["mode_max_eigenmode_x",5])
		self.var_list.append(["mode_max_eigenmode_y",5])
		self.var_list.append(["mode_te_tm","TE"])
		self.var_list.append(["mode_only_fundamental",False])
		self.var_list_build()

class json_mode_simulation(json_base):

	def __init__(self):
		json_base.__init__(self,"mode_segment")
		self.var_list=[]
		self.var_list.append(["name","Mode"])
		self.var_list.append(["icon","mode_fiber"])
		self.var_list.append(["config",json_mode_config()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_mode(json_base):

	def __init__(self):
		json_base.__init__(self,"mode",segment_class=True,segment_example=json_mode_simulation())
		self.var_list.append(["icon_","mode"])
		self.var_list_build()

