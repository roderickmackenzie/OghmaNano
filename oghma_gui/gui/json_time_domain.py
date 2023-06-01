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

## @package json_time_domain
#  Store the time domain json data
#

from json_base import json_base

class json_time_domain_mesh_segment(json_base):

	def __init__(self):
		json_base.__init__(self,"json_time_domain_mesh_segment")
		self.var_list=[]
		self.var_list.append(["len",10e-6])
		self.var_list.append(["dt",0.01e-6])
		self.var_list.append(["voltage_start",0.0])
		self.var_list.append(["voltage_stop",0.0])
		self.var_list.append(["mul",1.0])
		self.var_list.append(["sun_start",0.0])
		self.var_list.append(["sun_stop",0.0])
		self.var_list.append(["laser_start",0.0])
		self.var_list.append(["laser_stop",0.0])
		self.var_list_build()

class json_time_domain_mesh(json_base):

	def __init__(self):
		json_base.__init__(self,"mesh",segment_class=True,segment_example=json_time_domain_mesh_segment())
		self.var_list=[]
		self.var_list.append(["time_loop",False])
		self.var_list.append(["time_loop_times",4])
		self.var_list.append(["time_loop_reset_time",False])
		self.var_list_build()


class json_time_domain_config(json_base):

	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["pulse_shift",5e-6])
		self.var_list.append(["load_type","load"])
		self.var_list.append(["pulse_L",0.0])
		self.var_list.append(["Rload",0.0])
		self.var_list.append(["pump_laser","green"])
		self.var_list.append(["pulse_bias",0.0])
		self.var_list.append(["pulse_light_efficiency",1.0])
		self.var_list.append(["pulse_subtract_dc","false"])
		self.var_list.append(["start_time",-4e-12])
		self.var_list.append(["fs_laser_time",-1.0])
		self.var_list.append(["text_output_",""])
		self.var_list.append(["dump_verbosity",1])
		self.var_list.append(["dump_energy_space","false"])
		self.var_list.append(["dump_x",0])
		self.var_list.append(["dump_y",0])
		self.var_list.append(["dump_z",0])
		self.var_list_build()



class json_time_domain_simulation(json_base):

	def __init__(self):
		json_base.__init__(self,"time_domain_segment")
		self.var_list=[]
		self.var_list.append(["name","celiv"])
		self.var_list.append(["icon","celiv"])
		self.var_list.append(["config",json_time_domain_config()])
		self.var_list.append(["mesh",json_time_domain_mesh()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_time_domain(json_base):

	def __init__(self):
		json_base.__init__(self,"time_domain",segment_class=True,segment_example=json_time_domain_simulation())
		self.var_list.append(["icon_","celiv"])
		self.var_list_build()
