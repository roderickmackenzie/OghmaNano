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

## @package json_exciton
#  Store the exciton data
#


from json_base import json_base

class json_exciton_boundary(json_base):

	def __init__(self):
		json_base.__init__(self,"exciton_boundary")
		self.var_list=[]
		self.var_list.append(["y0_boundry","neumann"])
		self.var_list.append(["n_y0",1e24])
		self.var_list.append(["excitonsink_y0",100.0])
		self.var_list.append(["excitonsink_length_y0",1e-3])
		self.var_list.append(["y1_boundry","heatsink"])
		self.var_list.append(["n_y1",1e24])
		self.var_list.append(["excitonsink_y1",0.1])
		self.var_list.append(["excitonsink_length_y1",1e-2])
		self.var_list.append(["x0_boundry","neumann"])
		self.var_list.append(["n_x0",1e24])
		self.var_list.append(["excitonsink_x0",0.1])
		self.var_list.append(["excitonsink_length_x0",0.1])
		self.var_list.append(["x1_boundry","neumann"])
		self.var_list.append(["n_x1",1e24])
		self.var_list.append(["excitonsink_x1",200])
		self.var_list.append(["excitonsink_length_x1",0.1])
		self.var_list.append(["z0_boundry","neumann"])
		self.var_list.append(["n_z0",1e24])
		self.var_list.append(["excitonsink_z0",200])
		self.var_list.append(["excitonsink_length_z0",0.1])
		self.var_list.append(["z1_boundry","neumann"])
		self.var_list.append(["n_z1",1e24])
		self.var_list.append(["excitonsink_z1",200])
		self.var_list.append(["excitonsink_length_z1",0.1])
		self.var_list_build()

class json_exciton_config(json_base):

	def __init__(self):
		json_base.__init__(self,"exciton_config")
		self.var_list=[]
		self.var_list.append(["test","JV\\ncurve"])
		self.var_list_build()

class json_exciton_simulation(json_base):

	def __init__(self):
		json_base.__init__(self,"exciton_segment")
		self.var_list=[]
		self.var_list.append(["name","Exciton"])
		self.var_list.append(["icon","exciton"])
		self.var_list.append(["config",json_exciton_config()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_exciton_main(json_base):

	def __init__(self):
		json_base.__init__(self,"exciton",segment_class=True,segment_example=json_exciton_simulation())
		#This segment class should no longer be used it have moved to the sims structure
		#remove after 06/11/2024
		self.var_list=[]
		self.var_list.append(["exciton_enabled",False])
		self.var_list.append(["exciton_max_ittr",20])
		self.var_list.append(["exciton_min_error",1e-7])
		self.var_list.append(["dump_verbosity",1])
		self.var_list.append(["solver_verbosity","solver_verbosity_nothing"])
		self.var_list.append(["exciton_boundary",json_exciton_boundary()])
		self.var_list_build()

class json_exciton(json_base):

	def __init__(self):
		json_base.__init__(self,"exciton",segment_class=True,segment_example=json_exciton_simulation())



