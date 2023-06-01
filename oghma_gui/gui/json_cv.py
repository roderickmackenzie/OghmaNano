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

## @package json_cv_domain
#  Store the cv domain json data
#


from json_base import json_base


class json_cv_domain_config(json_base):

	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["cv_start_voltage",-2.0])
		self.var_list.append(["cv_stop_voltage",0.5])
		self.var_list.append(["cv_dv_step",0.1])
		self.var_list.append(["cv_fx",1000])
		self.var_list.append(["load_type","load"])
		self.var_list.append(["fxdomain_large_signal",True])
		self.var_list.append(["fxdomain_Rload",0.0])
		self.var_list.append(["fxdomain_points",30])
		self.var_list.append(["fxdomain_n",5])
		self.var_list.append(["fx_modulation_type","voltage"])
		self.var_list.append(["fxdomain_measure","measure_current"])
		self.var_list.append(["fxdomain_voltage_modulation_max",0.01])
		self.var_list.append(["fxdomain_light_modulation_depth",0.01])
		self.var_list.append(["fxdomain_do_fit",True])
		self.var_list.append(["fxdomain_L",0.0])
		self.var_list.append(["periods_to_fit",2])
		self.var_list.append(["fxdomain_modulation_rolloff_enable",False])
		self.var_list.append(["fxdomain_modulation_rolloff_start_fx",1e3])
		self.var_list.append(["fxdomain_modulation_rolloff_speed",1.6026e-05])
		self.var_list.append(["fxdomain_norm_tx_function",False])
		self.var_list.append(["dump_verbosity",0])
		self.var_list.append(["dump_screen_verbosity","dump_verbosity_key_results"])
		self.var_list_build()



class json_cv_domain_simulation(json_base):

	def __init__(self):
		json_base.__init__(self,"cv_domain_segment")
		self.var_list=[]
		self.var_list.append(["name","CV"])
		self.var_list.append(["icon","cv"])
		self.var_list.append(["config",json_cv_domain_config()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_cv(json_base):

	def __init__(self):
		json_base.__init__(self,"cv",segment_class=True,segment_example=json_cv_domain_simulation())
		self.var_list.append(["icon_","cv"])
		self.var_list_build()
