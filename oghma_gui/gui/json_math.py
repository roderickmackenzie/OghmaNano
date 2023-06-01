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

## @package json_math
#  Store the cv domain json data
#

from json_base import json_base

class json_math(json_base):

	def __init__(self):
		json_base.__init__(self,"math")
		self.var_list=[]
		self.var_list.append(["text_newton_first_itt_",""])
		self.var_list.append(["maxelectricalitt_first",1000])
		self.var_list.append(["electricalclamp_first",0.1])
		self.var_list.append(["math_electrical_error_first",1e-9])
		self.var_list.append(["newton_first_temperature_ramp",False])

		self.var_list.append(["text_newton_later_itt",""])
		self.var_list.append(["maxelectricalitt",100])
		self.var_list.append(["electricalclamp",1.0])
		self.var_list.append(["electricalerror",1e-8])

		self.var_list.append(["text_newton_exit_strategy_",""])
		self.var_list.append(["newton_clever_exit",True])
		self.var_list.append(["newton_min_itt",5])
		self.var_list.append(["remesh",0])
		self.var_list.append(["newmeshsize",8])
		self.var_list.append(["kl_in_newton",1])

		self.var_list.append(["text_newton_solver_type_",""])
		self.var_list.append(["solver_name","umfpack"])
		self.var_list.append(["newton_name","newton"])
		self.var_list.append(["complex_solver_name","complex_umfpack"])
		self.var_list.append(["math_t0",300.0])
		self.var_list.append(["math_d0",243.75])
		self.var_list.append(["math_n0",1e20])
		self.var_list.append(["math_current_calc_at","contacts"])

		self.var_list.append(["text_newton_output_",""])
		self.var_list.append(["math_dynamic_mesh",False])
		self.var_list.append(["math_stop_on_convergence_problem",False])
		self.var_list.append(["math_stop_on_inverted_fermi_level",False])
		self.var_list.append(["solver_verbosity","solver_verbosity_at_end"])
		self.var_list_build()

