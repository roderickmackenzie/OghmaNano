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


class json_fdtd_simulation(json_base):

	def __init__(self):
		json_base.__init__(self,"fdtd_segment")
		self.var_list=[]
		self.var_list.append(["name","FDTD"])
		self.var_list.append(["icon","fdtd"])
		self.var_list.append(["text_excitation",""])
		self.var_list.append(["fdtd_excitation_type","sin"])
		self.var_list.append(["fdtd_lambda_start",520e-9])
		self.var_list.append(["fdtd_lambda_stop",525e-9])
		self.var_list.append(["fdtd_lambda_points",1])
		self.var_list.append(["fdtd_pulse_length",100])
		self.var_list.append(["fdtd_excite_Ex",False])
		self.var_list.append(["fdtd_excite_Ey",True])
		self.var_list.append(["fdtd_excite_Ez",False])

		self.var_list.append(["text_fdtd_time",""])
		self.var_list.append(["fdtd_max_time",0.1])
		self.var_list.append(["fdtd_max_steps",10000])
		self.var_list.append(["lam_jmax",12])
		self.var_list.append(["text_fdtd_mesh",""])
		self.var_list.append(["fdtd_xzy","zy"])
		self.var_list.append(["fdtd_zlen",60])
		self.var_list.append(["fdtd_xlen",1])
		self.var_list.append(["fdtd_ylen",60])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_fdtd(json_base):

	def __init__(self):
		json_base.__init__(self,"fdtd",segment_class=True,segment_example=json_fdtd_simulation())
		self.var_list.append(["icon_","fdtd"])
		self.var_list_build()

