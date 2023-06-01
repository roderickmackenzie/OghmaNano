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

## @package json_ml
#  Machine learning 
#

from json_base import json_base
from json_fit import json_fit_duplicate

#############

class json_duplicate_line(json_base):

	def __init__(self):
		json_base.__init__(self,"segment")
		self.var_list=[]
		self.var_list.append(["duplicate_var_enabled",True])
		self.var_list.append(["human_src","one/two/three"])
		self.var_list.append(["human_dest","one/two/three"])
		self.var_list.append(["multiplier","x"])
		self.var_list.append(["json_src","one/two/three"])
		self.var_list.append(["json_dest","one/two/three"])
		self.var_list_build()

class json_ml_random_item(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_random_item")
		self.var_list=[]
		self.var_list.append(["random_var_enabled",True])
		self.var_list.append(["json_var","one/two/three"])
		self.var_list.append(["human_var","one/two/three"])
		self.var_list.append(["min",0.0])
		self.var_list.append(["max",1.0])
		self.var_list.append(["random_distribution","log"])
		self.var_list_build()

class json_ml_random(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_random",segment_class=True,segment_example=json_ml_random_item())

####################

class json_ml_output_vector_item(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_output_vector_item")
		self.var_list=[]
		self.var_list.append(["ml_output_vector_item_enabled",True])
		self.var_list.append(["file_name","jv.dat"])
		self.var_list.append(["ml_token_name","jv_light"])
		self.var_list.append(["vectors","0.0,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0"])
		self.var_list_build()


class json_ml_output_vectors(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_output_vectors",segment_class=True,segment_example=json_ml_output_vector_item())


####################

class json_ml_patch_item(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_patch")
		self.var_list=[]
		self.var_list.append(["ml_patch_enabled",True])
		self.var_list.append(["json_var","one/two/three"])
		self.var_list.append(["human_var","one/two/three"])
		self.var_list.append(["ml_patch_val","value"])
		self.var_list_build()


class json_ml_patch(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_patch",segment_class=True,segment_example=json_ml_patch_item())


###############

class json_ml_sims_item(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_sims_item")
		self.var_list=[]
		self.var_list.append(["ml_sim_enabled",True])
		self.var_list.append(["sim_name","segment0@jv"])
		self.var_list.append(["ml_patch",json_ml_patch()])
		self.var_list.append(["ml_output_vectors",json_ml_output_vectors()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()

class json_ml_sims(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_sims",segment_class=True,segment_example=json_ml_sims_item())


##############

class json_ml_config(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_config")
		self.var_list=[]
		self.var_list.append(["ml_number_of_archives",400])
		self.var_list.append(["ml_sims_per_archive",40])
		self.var_list.append(["ml_archive_path","cwd"])
		self.var_list.append(["ml_vector_file_name","vectors.json"])
		self.var_list_build()

class json_ml_segment(json_base):

	def __init__(self):
		json_base.__init__(self,"ml_segment")
		self.var_list=[]
		self.var_list.append(["name","ML"])
		self.var_list.append(["icon","ml"])
		self.var_list.append(["ml_random",json_ml_random()])
		self.var_list.append(["ml_patch",json_ml_patch()])
		self.var_list.append(["duplicate",json_fit_duplicate()])
		self.var_list.append(["ml_sims",json_ml_sims()])
		self.var_list.append(["ml_config",json_ml_config()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_ml(json_base):

	def __init__(self):
		json_base.__init__(self,"ml",segment_class=True,segment_example=json_ml_segment())


