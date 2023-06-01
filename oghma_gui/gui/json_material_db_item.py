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

## @package json_shape_db_item
#  Store the shape information
#


from json_base import json_base
from json_import_config import json_import_config
from json_dos import json_dos

class json_material_db_electrical_constants(json_base):

	def __init__(self):
		json_base.__init__(self,"electrical_constants")
		self.var_list=[]
		self.var_list.extend(json_dos().gen_var_list(material_db=True))
		self.var_list.append(["material_blend",False])
		self.var_list.append(["Xi0",-3.0])
		self.var_list.append(["Eg0",1.0])
		self.var_list.append(["Xi1",-3.0])
		self.var_list.append(["Eg1",1.0])
		self.var_list_build()
		self.srh_bands=0

class json_material_db_thermal_constants(json_base):

	def __init__(self):
		json_base.__init__(self,"thermal_constants")
		self.var_list=[]
		self.var_list.append(["thermal_kl",1.0])
		self.var_list.append(["thermal_tau_e",1.0000e-8])
		self.var_list.append(["thermal_tau_h",1.0000e-9])
		self.var_list_build()

class json_material_db_lca(json_base):

	def __init__(self):
		json_base.__init__(self,"lca")
		self.var_list=[]
		self.var_list.append(["lca_density",2400])
		self.var_list.append(["lca_cost",0.47])
		self.var_list.append(["lca_energy",37450374.430606])
		self.var_list_build()

class json_material_db_item(json_base):

	def __init__(self):
		json_base.__init__(self,"material_db_item")
		self.var_list=[]
		self.var_list.append(["item_type","material"])
		self.var_list.append(["color_r",0.8])
		self.var_list.append(["color_g",0.8])
		self.var_list.append(["color_b",0.8])
		self.var_list.append(["color_alpha",0.8])
		self.var_list.append(["material_type","other"])
		self.var_list.append(["status","private"])
		self.var_list.append(["changelog",""])
		self.var_list.append(["mat_src",""])
		self.var_list.append(["n_import",json_import_config(name="n_import")])
		self.var_list.append(["alpha_import",json_import_config(name="alpha_import")])
		self.var_list.append(["emission_import",json_import_config(name="emission_import")])
		self.var_list.append(["electrical_constants",json_material_db_electrical_constants()])
		self.var_list.append(["thermal_constants",json_material_db_thermal_constants()])
		self.var_list.append(["lca",json_material_db_lca()])
		self.var_list_build()
		self.include_name=False

class json_material_db_sub_folder(json_base):

	def __init__(self):
		json_base.__init__(self,"material_db_sub_folder")
		self.var_list=[]
		self.var_list.append(["item_type","material_sub_folder"])
		self.var_list.append(["ver",1.0])
		self.var_list_build()
		self.include_name=False

