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

## @package json_light
#  Store the cv domain json data
#

from json_base import json_base


class json_light_spectrum(json_base):

	def __init__(self):
		json_base.__init__(self,"light_spectrum")
		self.var_list=[]
		self.var_list.append(["light_spectrum","AM1.5G"])
		self.var_list.append(["light_multiplyer",1.0])
		self.var_list_build()


class json_light_external_interface(json_base):

	def __init__(self):
		json_base.__init__(self,"external_interface")
		self.var_list=[]
		self.var_list.append(["enabled",False])
		self.var_list.append(["light_external_n",1.0])
		self.var_list_build()


class json_light_spectra(json_base):

	def __init__(self):
		json_base.__init__(self,"light_spectra",segment_class=True,segment_example=json_light_spectrum())


class json_filter_spectrum(json_base):

	def __init__(self):
		json_base.__init__(self,"light_filter")
		self.var_list=[]
		self.var_list.append(["filter_enabled",False])
		self.var_list.append(["filter_material","glasses/glass"])
		self.var_list.append(["filter_invert",True])
		self.var_list.append(["filter_db",1000.0])

		self.var_list_build()

class json_light_filters(json_base):

	def __init__(self):
		json_base.__init__(self,"light_filters",segment_class=True,segment_example=json_filter_spectrum())

class json_virtual_spectra(json_base):

	def __init__(self,name):
		json_base.__init__(self,name)
		self.var_list=[]
		self.var_list.append(["light_spectra",json_light_spectra()])
		self.var_list.append(["light_filters",json_light_filters()])
		self.var_list.append(["external_interface",json_light_external_interface()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_light(json_base):

	def __init__(self):
		json_base.__init__(self,"light")
		self.var_list=[]
		self.var_list.append(["light_model","full"])
		self.var_list.append(["Psun",1.0])
		self.var_list.append(["sun","AM1.5G"])
		self.var_list.append(["Dphotoneff",1.0])
		self.var_list.append(["NDfilter",0.000000e+00])
		self.var_list.append(["light_flat_generation_rate",2e28])
		self.var_list.append(["light_file_generation","Gn.inp"])
		self.var_list.append(["light_file_qe_spectra",""])
		self.var_list.append(["light_file_generation_shift",200e-9])
		self.var_list.append(["dump_verbosity",10])
		self.var_list_build()
		self.latex_banned=["all"]
		self.latex_allowed=["Dphotoneff"]
