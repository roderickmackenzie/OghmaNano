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

## @package json_jv
#  Store the cv domain json data
#

from json_base import json_base


class json_jv_config(json_base):

	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["Vstart",0.0])
		self.var_list.append(["Vstop",1.2])
		self.var_list.append(["Vstep",0.01])
		self.var_list.append(["jv_step_mul",1.00])
		self.var_list.append(["jv_use_external_voltage_as_stop",True])
		self.var_list.append(["jv_light_efficiency",1.0])
		self.var_list.append(["jv_max_j",1e3])
		self.var_list.append(["jv_Rcontact",-1.0])
		self.var_list.append(["jv_Rshunt",-1.0])
		self.var_list.append(["jv_single_point",False])
		self.var_list.append(["text_output_",""])
		self.var_list.append(["dump_verbosity",1])
		self.var_list.append(["dump_energy_space","false"])
		self.var_list.append(["dump_x",0])
		self.var_list.append(["dump_y",0])
		self.var_list.append(["dump_z",0])
		self.var_list_build()



class json_jv_simulation(json_base):

	def __init__(self):
		json_base.__init__(self,"jv_segment")
		self.var_list=[]
		self.var_list.append(["name","JV\\ncurve"])
		self.var_list.append(["icon","jv"])
		self.var_list.append(["config",json_jv_config()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_jv(json_base):

	def __init__(self):
		json_base.__init__(self,"jv",segment_class=True,segment_example=json_jv_simulation())
		self.var_list=[]
		self.var_list.append(["icon_","jv"])
		self.var_list_build()

