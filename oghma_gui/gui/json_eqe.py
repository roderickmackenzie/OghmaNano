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


class json_eqe_simulation(json_base):

	def __init__(self):
		json_base.__init__(self,"eqe_segment")
		self.var_list=[]
		self.var_list.append(["name","EQE"])
		self.var_list.append(["icon","qe"])
		self.var_list.append(["eqe_voltage",-20.0])
		self.var_list.append(["eqe_light_power2",1.0])
		self.var_list.append(["eqe_single_light_point",True])
		self.var_list.append(["eqe_suns_start",1e-3])
		self.var_list.append(["eqe_suns_stop",1.0])
		self.var_list.append(["eqe_wavelength",532e-9])
		self.var_list.append(["eqe_use_electrical_dos",False])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_eqe(json_base):

	def __init__(self):
		json_base.__init__(self,"eqe",segment_class=True,segment_example=json_eqe_simulation())
		self.var_list.append(["icon_","qe"])
		self.var_list_build()
