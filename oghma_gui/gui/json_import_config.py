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

## @package json_import_config
#  Used to store json_base
#


from json_base import json_base

class json_import_config(json_base):

	def __init__(self,name="import_config"):
		json_base.__init__(self,name)
		self.var_list=[]
		self.var_list.append(["import_file_path","none"])
		self.var_list.append(["import_x_combo_pos",9])
		self.var_list.append(["import_data_combo_pos",5])
		self.var_list.append(["import_x_spin",0])
		self.var_list.append(["import_data_spin",1])
		self.var_list.append(["import_title","Voltage - J"])
		self.var_list.append(["import_xlabel","Voltage"])
		self.var_list.append(["import_data_label","J"])
		self.var_list.append(["import_area",0.104])
		self.var_list.append(["import_data_invert",False])
		self.var_list.append(["import_x_invert",False])
		self.var_list.append(["data_file","none"])
		self.var_list_build()


