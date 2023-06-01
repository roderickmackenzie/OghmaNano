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

## @package json_thermal
#  Store the thermal data
#

from json_base import json_base
from json_mesh import json_mesh

#class json_thermal_range(json_base):

#	def __init__(self):
#		json_base.__init__(self,"thermal_range")
#		self.var_list=[]
#		self.var_list.append(["T_mesh_force",False])
#		self.var_list.append(["T_min",300.0])
#		self.var_list.append(["T_max",305.0])
#		self.var_list.append(["Tpoints",1])
#		self.var_list_build()

class json_thermal_boundary(json_base):

	def __init__(self):
		json_base.__init__(self,"thermal_boundary")
		self.var_list=[]
		self.var_list.append(["y0_boundry","neumann"])
		self.var_list.append(["Ty0",300.0])
		self.var_list.append(["heatsink_y0",100.0])
		self.var_list.append(["heatsink_length_y0",1e-3])
		self.var_list.append(["y1_boundry","heatsink"])
		self.var_list.append(["Ty1",300.0])
		self.var_list.append(["heatsink_y1",0.1])
		self.var_list.append(["heatsink_length_y1",1e-2])
		self.var_list.append(["x0_boundry","neumann"])
		self.var_list.append(["Tx0",300.0])
		self.var_list.append(["heatsink_x0",0.1])
		self.var_list.append(["heatsink_length_x0",0.1])
		self.var_list.append(["x1_boundry","neumann"])
		self.var_list.append(["Tx1",300.0])
		self.var_list.append(["heatsink_x1",200])
		self.var_list.append(["heatsink_length_x1",0.1])
		self.var_list.append(["z0_boundry","neumann"])
		self.var_list.append(["Tz0",300.0])
		self.var_list.append(["heatsink_z0",200])
		self.var_list.append(["heatsink_length_z0",0.1])
		self.var_list.append(["z1_boundry","neumann"])
		self.var_list.append(["Tz1",300.0])
		self.var_list.append(["heatsink_z1",200])
		self.var_list.append(["heatsink_length_z1",0.1])
		self.var_list_build()

class json_thermal(json_base):

	def __init__(self):
		json_base.__init__(self,"thermal")
		self.var_list=[]
		self.var_list.append(["icon_","thermal"])
		self.var_list.append(["set_point",300.0])
		self.var_list.append(["mesh",json_mesh(x=False,y=False,z=False,t=True)])
		self.var_list.append(["thermal_boundary",json_thermal_boundary()])
		self.var_list.append(["thermal",False])
		self.var_list.append(["thermal_model_type","thermal_lattice"])
		self.var_list.append(["thermal_l","true"])
		self.var_list.append(["thermal_e","false"])
		self.var_list.append(["thermal_h","false"])
		self.var_list.append(["nofluxl",1])
		self.var_list.append(["thermal_max_ittr",20])
		self.var_list.append(["thermal_min_error",1e-7])
		self.var_list.append(["joule_heating",True])
		self.var_list.append(["parasitic_heating",True])
		self.var_list.append(["thermal_couple_to_electrical_solver",True])
		self.var_list.append(["recombination_heating",False])
		self.var_list.append(["optical_heating",False])
		self.var_list.append(["dump_verbosity",1])
		self.var_list.append(["solver_verbosity","solver_verbosity_nothing"])
		self.var_list_build()




