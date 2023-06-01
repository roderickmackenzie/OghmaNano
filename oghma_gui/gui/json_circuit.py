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

## @package json_circuit
#  Store the cv domain json data
#

from json_base import json_base


class json_component(json_base):

	def __init__(self):
		json_base.__init__(self,"component")
		self.var_list=[]
		self.var_list.append(["name","component"])
		self.var_list.append(["comp","resistor"])
		self.var_list.append(["x0",2])
		self.var_list.append(["y0",2])
		self.var_list.append(["x1",3])
		self.var_list.append(["y1",3])
		self.var_list.append(["R",10.0])
		self.var_list.append(["C",0.0])
		self.var_list.append(["L",0.0])
		self.var_list.append(["a",1e-3])
		self.var_list.append(["b",1e-3])
		self.var_list.append(["c",1e-3])
		self.var_list.append(["nid",1.0])
		self.var_list.append(["I0",1e-12])
		self.var_list.append(["layer","none"])
		self.var_list.append(["Dphotoneff",1.0])
		self.var_list_build()

		self.dir="north"
		self.lines=[]

	def __str__(self):
		return str(self.x0)+" "+str(self.y0)+" "+str(self.x1)+" "+str(self.y1)+" "+self.name

	def __eq__(self,a):
		if self.x0==a.x0:
			if self.y0==a.y0:
				if self.x1==a.x1:
					if self.y1==a.y1:
						return True

		if self.x0==a.x1:
			if self.y0==a.y1:
				if self.x1==a.x0:
					if self.y1==a.y0:
						return True
		return False

	def get_direction(self):
		if self.x0==self.x1:
			if self.y1>self.y0:
				return "up"
			else:
				return "down"

		if self.y0==self.y1:
			if self.x1>self.x0:
				return "right"
			else:
				return "left"

class json_circuit_diagram(json_base):

	def __init__(self):
		json_base.__init__(self,"circuit_diagram",segment_class=True,segment_example=json_component())


class json_circuit_config(json_base):

	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["solver_verbosity","solver_verbosity_at_end"])
		self.var_list_build()

		self.dir="north"
		self.lines=[]

class json_circuit(json_base):

	def __init__(self):
		json_base.__init__(self,"circuit")
		self.var_list=[]
		self.var_list.append(["enabled",False])
		self.var_list.append(["icon_","kirchhoff"])
		self.var_list.append(["circuit_diagram",json_circuit_diagram()])
		self.var_list.append(["config",json_circuit_config()])
		self.var_list_build()


