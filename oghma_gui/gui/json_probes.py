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

## @package json_probes
#  Machine learning 
#

from json_base import json_base

###############

class json_probe_item(json_base):

	def __init__(self):
		json_base.__init__(self,"probe_item")
		self.var_list=[]
		self.var_list.append(["probe_enabled",True])
		self.var_list.append(["probe_type","point"])
		self.var_list.append(["file_name","Ec.csv"])
		self.var_list.append(["px",0])
		self.var_list.append(["py",0])
		self.var_list.append(["pz",0])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()

class json_probes(json_base):

	def __init__(self):
		json_base.__init__(self,"probes",segment_class=True,segment_example=json_probe_item())


class json_probe_block(json_base):

	def __init__(self):
		json_base.__init__(self,"probe")
		self.var_list=[]
		self.var_list.append(["name","probe"])
		self.var_list.append(["icon_","map_pin"])
		self.var_list.append(["probes",json_probes()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_all_probes(json_base):

	def __init__(self):
		json_base.__init__(self,"probes",segment_class=True,segment_example=json_probe_block())


