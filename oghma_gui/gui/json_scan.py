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

## @package json_scan
#  Sacns
#

from json_base import json_base

class json_scan_line(json_base):

	def __init__(self):
		json_base.__init__(self,"json_scan_line")
		self.hex=["values","opp"]
		self.var_list=[]
		self.var_list.append(["human_var",_("Paramter to change")])
		self.var_list.append(["values","values"])
		self.var_list.append(["opp","scan"])
		self.var_list.append(["token_json",_("Paramter to change")])
		self.var_list.append(["token_json1", "token_json1"])
		self.var_list_build()

class json_scan_optimizer(json_base):

	def __init__(self):
		json_base.__init__(self,"scan_optimizer")
		self.var_list=[]
		self.var_list.append(["enabled",False])
		self.var_list.append(["scan_optimizer_dump_at_end",False])
		self.var_list.append(["scan_optimizer_dump_n_steps",300])
		self.var_list_build()

class json_scan(json_base):

	def __init__(self):
		json_base.__init__(self,"scan",segment_class=True,segment_example=json_scan_line())
		self.var_list=[]
		self.var_list.append(["icon","scan"])
		self.var_list.append(["name","name"])
		self.var_list.append(["scan_optimizer",json_scan_optimizer()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_scan_config(json_base):

	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["none","none"])
		self.var_list_build()


class json_scans(json_base):

	def __init__(self):
		json_base.__init__(self,"scans",segment_class=True,segment_example=json_scan())
		self.var_list=[]
		self.var_list.append(["config",json_scan_config()])
		self.var_list_build()


