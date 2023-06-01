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

## @package json_server
#  Store the cv domain json data
#

from json_base import json_base


class json_server(json_base):

	def __init__(self):
		json_base.__init__(self,"server")
		self.var_list=[]
		self.var_list.append(["text_cpu",""])
		self.var_list.append(["core_max_threads",0])
		self.var_list.append(["server_stall_time",2000])
		self.var_list.append(["server_max_run_time",345600])
		self.var_list.append(["server_min_cpus",1])
		self.var_list.append(["server_steel",0])
		self.var_list.append(["server_use_dos_disk_cache",True])
		self.var_list.append(["max_core_instances",0])
		self.var_list.append(["text_gpu",""])
		self.var_list.append(["use_gpu",False])
		self.var_list.append(["gpu_name","none"])
		self.var_list_build()


