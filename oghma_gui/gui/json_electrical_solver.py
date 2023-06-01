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

## @package json_electrical_solver
#  Store the electrical solver domain json data
#


from json_base import json_base
from json_poisson import json_poisson
from json_mesh import json_mesh

class json_electrical_cache(json_base):

	def __init__(self):
		json_base.__init__(self,"cache")
		self.var_list=[]
		self.var_list.append(["cache_max_size",200])
		self.var_list.append(["cache_disk_speed",408])
		self.var_list.append(["cache_enabled",False])
		self.var_list.append(["cache_path","none_none_none_default"])
		self.var_list_build()

class json_electrical_boundary(json_base):

	def __init__(self):
		json_base.__init__(self,"boundary")
		self.var_list=[]
		self.var_list.append(["electrical_y0_boundry","neumann"])
		self.var_list.append(["electrical_y0",0.0])
		self.var_list.append(["electrical_y1_boundry","neumann"])
		self.var_list.append(["electrical_y1",0.0])
		self.var_list.append(["electrical_x0_boundry","neumann"])
		self.var_list.append(["electrical_x0",0.0])
		self.var_list.append(["electrical_x1_boundry","neumann"])
		self.var_list.append(["electrical_x1",0.0])
		self.var_list_build()

class json_electrical_solver(json_base):

	def __init__(self):
		json_base.__init__(self,"electrical_solver")
		self.var_list=[]
		self.var_list.append(["icon_","drift_diffusion"])
		self.var_list.append(["solver_type","drift-diffusion"])
		self.var_list.append(["boundary",json_electrical_boundary()])
		self.var_list.append(["poisson",json_poisson()])
		self.var_list.append(["mesh",json_mesh()])
		self.var_list.append(["cache",json_electrical_cache()])
		self.var_list_build()



