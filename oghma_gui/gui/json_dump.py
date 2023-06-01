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

## @package json_dump
#  Store the cv domain json data
#


from json_base import json_base
from json_probes import json_all_probes


class json_banned_file(json_base):

	def __init__(self):
		json_base.__init__(self,"banned_file")
		self.var_list=[]
		self.var_list.append(["banned_enabled","True"])
		self.var_list.append(["banned_file_name","jv.dat"])
		self.var_list_build()


class json_banned_files(json_base):

	def __init__(self):
		json_base.__init__(self,"banned_files",segment_class=True,segment_example=json_banned_file())

class json_dump(json_base):

	def __init__(self):
		json_base.__init__(self,"dump")
		self.var_list=[]
		self.var_list.append(["dump_dynamic",False])
		self.var_list.append(["dump_write_converge",True])
		self.var_list.append(["dump_norm_time_to_one",False])
		self.var_list.append(["dump_norm_y_axis",False])
		self.var_list.append(["dump_write_out_band_structure",0])
		self.var_list.append(["dump_first_guess",False])
		self.var_list.append(["dump_log_level","screen_and_disk"])
		self.var_list.append(["dump_optical_probe",False])
		self.var_list.append(["dump_optical_probe_spectrum",False])
		self.var_list.append(["dump_print_text",0])
		self.var_list.append(["dump_write_headers",True])
		self.var_list.append(["dump_remove_dos_cache",False])
		self.var_list.append(["dump_dynamic_pl_energy",False])
		self.var_list.append(["dump_binary",True])
		self.var_list.append(["banned_files",json_banned_files()])
		self.var_list.append(["probes",json_all_probes()])
		self.var_list_build()






