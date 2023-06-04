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

## @package shape
#  Shape object file.
#

import os
from str2bool import str2bool

from vec import vec
from json_base import json_base
from json_electrical import json_electrical
from math import fabs
from json_world_object import json_world_object
import copy
from json_dos import json_dos

class shape_pl(json_base):
	def __init__(self):
		json_base.__init__(self,"shape_pl")
		self.var_list=[]
		self.var_list.append(["pl_emission_enabled",False])
		self.var_list.append(["pl_use_experimental_emission_spectra",False])
		self.var_list.append(["pl_input_spectrum","none"])
		self.var_list.append(["pl_experimental_emission_efficiency",1.0])
		self.var_list.append(["pl_fe_fh",1.0])
		self.var_list.append(["pl_fe_te",1.0])
		self.var_list.append(["pl_te_fh",1.0])
		self.var_list.append(["pl_th_fe",1.0])
		self.var_list.append(["pl_fh_th",1.0])
		self.var_list.append(["text_ray_tracing",False])
		self.var_list.append(["ray_theta_steps",200])
		self.var_list.append(["ray_theta_start",0])
		self.var_list.append(["ray_theta_stop",360])
		self.var_list.append(["ray_phi_steps",5])
		self.var_list.append(["ray_phi_start",0])
		self.var_list.append(["ray_phi_stop",360])
		self.var_list.append(["ray_emission_source","ray_emission_single_point"])
		self.var_list.append(["ray_super_sample_x",False])
		self.var_list.append(["ray_super_sample_x_points",4])
		self.var_list_build()

class shape_heat(json_base):
	def __init__(self):
		json_base.__init__(self,"shape_heat")
		self.var_list=[]
		self.var_list.append(["thermal_kl",1.0])
		self.var_list.append(["thermal_tau_e",1.0])
		self.var_list.append(["thermal_tau_h",1.0])
		self.var_list_build()

class shape_display_options(json_base):
	def __init__(self):
		json_base.__init__(self,"display_options")
		self.var_list=[]
		self.var_list.append(["show_solid",True])
		self.var_list.append(["show_mesh",True])
		self.var_list.append(["show_cut_through_x",False])
		self.var_list.append(["show_cut_through_y",False])
		self.var_list.append(["hidden",False])
		self.var_list_build()

class shape(json_base,json_world_object):

	def __init__(self):
		json_base.__init__(self,"shape",segment_class=True,segment_example=None)
		json_world_object.__init__(self)
		self.var_list.append(["display_options",shape_display_options()])
		self.var_list.append(["shape_dos",json_dos()])
		self.var_list.append(["shape_electrical",json_electrical()])

		self.var_list.append(["optical_material","blends/p3htpcbm"])
		self.var_list.append(["shape_pl",shape_pl()])
		self.var_list.append(["shape_heat",shape_heat()])
		self.var_list.append(["Gnp",0.0])
		self.var_list.append(["optical_thickness",0.0])
		self.var_list.append(["optical_thickness_enabled",False])
		self.var_list.append(["moveable",False])
		self.var_list_build()
		self.loaded_from_json=False


		self.segment_examples=[copy.deepcopy(self)]

	def decode_from_json(self,json):
		self.load_from_json(json)
		#self.enabled=str2bool(self.enabled)
		self.loaded_from_json=True
		#backwards compatability take out after 22/08/22
		if self.shape_dos.doping_start>0.0:
			self.shape_dos.Nd0=fabs(self.shape_dos.doping_start)
			self.shape_dos.Na0=0.0

		if self.shape_dos.doping_stop>0.0:
			self.shape_dos.Nd1=fabs(self.shape_dos.doping_stop)
			self.shape_dos.Na1=0.0

		if self.shape_dos.doping_start<0.0:
			self.shape_dos.Na0=fabs(self.shape_dos.doping_start)
			self.shape_dos.Nd0=0.0
			

		if self.shape_dos.doping_stop<0.0:
			self.shape_dos.Na1=fabs(self.shape_dos.doping_stop)
			self.shape_dos.Nd1=0.0

		self.shape_dos.doping_start=0.0
		self.shape_dos.doping_stop=0.0

		if self.optical_material=="metal/al":				#A patch remove after  08/12/2022
			self.optical_material="metal/Al/std"

		if self.optical_material=="metal/au":
			self.optical_material="metal/Au/std"

		if self.optical_material=="metal/ag":
			self.optical_material="metal/Ag/std"

		if self.optical_material=="oxides/ito":
			self.optical_material="oxides/ITO/ito"

		if self.optical_material=="oxides/ito_brabec":
			self.optical_material="oxides/ITO/ito_brabec"

		if self.optical_material=="oxides/zno":
			self.optical_material="oxides/ZnO/zno"

		if self.optical_material=="oxides/zno_china":
			self.optical_material="oxides/ZnO/zno_china"

		if self.optical_material=="oxides/zno_aunr_china":
			self.optical_material="oxides/ZnO/zno_aunr_china"



